
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Medicine


class MedicineAPITests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!"
        )

        self.client.force_authenticate(user=self.user)

        self.medicine = Medicine.objects.create(
            medicine_code="MED-1001",
            name="Paracetamol",
            generic_name="Paracetamol",
            manufacturer="ABC Pharma",
            strength="500 mg",
            dosage_form="Tablet",
            category="Pain Relief",
            prescription_required=False,
            is_active=True,
        )

        self.list_url = "/api/medicines/"
        self.detail_url = f"/api/medicines/{self.medicine.id}/"

    def test_list_medicines(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_medicine(self):
        data = {
            "medicine_code": "MED-1002",
            "name": "Cetirizine",
            "generic_name": "Cetirizine",
            "manufacturer": "XYZ Pharma",
            "strength": "10 mg",
            "dosage_form": "Tablet",
            "category": "Antihistamine",
            "prescription_required": False,
            "is_active": True,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Medicine.objects.filter(medicine_code="MED-1002").exists()
        )

    def test_duplicate_medicine_code(self):
        data = {
            "medicine_code": "MED-1001",
            "name": "Another Medicine",
            "generic_name": "Test Generic",
            "manufacturer": "Test Pharma",
            "strength": "20 mg",
            "dosage_form": "Tablet",
            "category": "Test",
            "prescription_required": False,
            "is_active": True,
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_retrieve_medicine(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Paracetamol")

    def test_update_medicine(self):
        response = self.client.patch(
            self.detail_url,
            {"name": "Paracetamol Updated"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.medicine.refresh_from_db()

        self.assertEqual(
            self.medicine.name,
            "Paracetamol Updated"
        )

    def test_delete_medicine(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Medicine.objects.filter(id=self.medicine.id).exists()
        )
