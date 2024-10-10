from django.shortcuts import render
import csv
from io import StringIO
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from datetime import datetime





class FileUploadView(APIView):

    def post(self, request):
        # Fetch uploaded files
        try:
            source_file = request.FILES['source']
            target_file = request.FILES['target']
        except KeyError:
            return HttpResponseBadRequest('Both source and target files are required.')

        try:
            # Normalize the data
            source_data = self.process_csv(source_file)
            target_data = self.process_csv(target_file)
        except ValidationError as e:
            return HttpResponseBadRequest(f'Invalid file format: {str(e)}')

        # Store data in session
        request.session['source_data'] = source_data
        request.session['target_data'] = target_data

        return JsonResponse({'message': 'Files uploaded and processed successfully.'})

    def process_csv(self, file):
        """Reads CSV file and returns normalized data in dictionary form."""
        try:
            file_data = file.read().decode('utf-8')
            csv_reader = csv.DictReader(StringIO(file_data))
            records = [self.normalize_row(row) for row in csv_reader]
            return records
        except Exception as e:
            raise ValidationError('Failed to parse CSV file.')

    def normalize_row(self, row):
        """Normalize data to handle data transformation issues."""
        normalized_row = {}

        for key, value in row.items():
            # strip spaces and convert to lowercase
            normalized_key = key.strip().lower()

            # strip leading/trailing spaces
            normalized_value = value.strip()

            # Normalize date formats
            if normalized_key == 'date':
                try:
                    parsed_date = datetime.strptime(normalized_value, "%m/%d/%Y")
                    normalized_value = parsed_date.strftime("%Y-%m-%d")  # Convert to YYYY-MM-DD
                except ValueError:
                    pass

            normalized_row[normalized_key] = normalized_value

        return normalized_row



class ReconciliationReportView(APIView):

    def get(self, request):
        # Fetch the normalized data from session
        source_data = request.session.get('source_data')
        target_data = request.session.get('target_data')

        if source_data is None or target_data is None:
            return HttpResponseBadRequest('No data available. Please upload files first.')

        # Perform reconciliation on files
        missing_in_target, missing_in_source, discrepancies = self.reconcile_data(source_data, target_data)

        return JsonResponse({
            'missing_in_target': missing_in_target,
            'missing_in_source': missing_in_source,
            'discrepancies': discrepancies
        })


    def reconcile_data(self, source_data, target_data):
        missing_in_target = []
        missing_in_source = []
        discrepancies = []

        # Create dictionaries by 'id'
        source_dict = {record['id']: record for record in source_data}
        target_dict = {record['id']: record for record in target_data}

        # Find records in source but missing in target
        for record_id, source_record in source_dict.items():
            if record_id not in target_dict:
                missing_in_target.append(source_record)

        # Find records in target but missing in source
        for record_id, target_record in target_dict.items():
            if record_id not in source_dict:
                missing_in_source.append(target_record)

        # Compare records that exist in both to find discrepancies
        for record_id in source_dict:
            if record_id in target_dict:
                source_record = source_dict[record_id]
                target_record = target_dict[record_id]
                record_discrepancies = {}

                # Compare each field in the records
                for field in source_record:
                    if field in target_record and source_record[field] != target_record[field]:
                        # Record the discrepancy
                        record_discrepancies[field] = {
                            'source_value': source_record[field],
                            'target_value': target_record[field]
                        }

                if record_discrepancies:
                    discrepancies.append({
                        'id': record_id,
                        'discrepancies': record_discrepancies
                    })

        return missing_in_target, missing_in_source, discrepancies