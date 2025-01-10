from django.db import models
import pandas as pd
import json

class CSVData(models.Model):
    file_name = models.CharField(max_length=255)
    data = models.TextField()  # Stocker les données sous forme de chaîne JSON
    csv_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    
    @classmethod
    def create_from_csv(cls, csv_file):
        # Lire le CSV avec Pandas
        df = pd.read_csv(csv_file)
        
        # Convertir le DataFrame en JSON
        json_data = df.to_json(orient='records')  # Convertir en chaîne JSON
        
        # Créer une nouvelle instance de CSVData
        instance = cls.objects.create(
            file_name=csv_file.name,
            data=json_data
        )
        return instance
