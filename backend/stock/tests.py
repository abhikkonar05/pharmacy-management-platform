
from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from medicines.models import Medicine
from batches.models import Batch
from stock.models import StockMovement
from stock.services import apply_stock_movement


class StockMovementServiceTests(TestCase):

    def setUp(self):
        self.medicine = Medicine.objects.create(
            medicine_code="TEST-1001",
            name="Test Paracetamol",
            generic_name="Paracetamol",
            manufacturer="Test Pharma",
            strength="500 mg",
            dosage_form="Tablet",
            category="Pain Relief",
            prescription_required=False,
            is_active=True,
        )

        self.batch = Batch.objects.create(
            medicine=self.medicine,
            batch_number="TEST-BATCH-001",
            manufacturing_date=date(2025, 1, 1),
            expiry_date=date(2027, 12, 31),
            purchase_price="10.00",
            selling_price="15.00",
            quantity_received=100,
            available_quantity=100,
        )

    def test_purchase_increases_stock(self):
        movement = apply_stock_movement(
            batch_id=self.batch.id,
            movement_type="PURCHASE",
            direction="IN",
            quantity=50,
        )

        self.batch.refresh_from_db()

        self.assertEqual(self.batch.available_quantity, 150)
        self.assertEqual(movement.quantity_before, 100)
        self.assertEqual(movement.quantity_after, 150)

    def test_sale_decreases_stock(self):
        movement = apply_stock_movement(
            batch_id=self.batch.id,
            movement_type="SALE",
            direction="OUT",
            quantity=20,
        )

        self.batch.refresh_from_db()

        self.assertEqual(self.batch.available_quantity, 80)
        self.assertEqual(movement.quantity_before, 100)
        self.assertEqual(movement.quantity_after, 80)

    def test_insufficient_stock_rejected(self):
        with self.assertRaises(ValidationError):
            apply_stock_movement(
                batch_id=self.batch.id,
                movement_type="SALE",
                direction="OUT",
                quantity=150,
            )

        self.batch.refresh_from_db()

        self.assertEqual(self.batch.available_quantity, 100)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_expired_batch_sale_rejected(self):
        self.batch.expiry_date = date(2025, 12, 31)
        self.batch.save(update_fields=["expiry_date"])

        with self.assertRaises(ValidationError):
            apply_stock_movement(
                batch_id=self.batch.id,
                movement_type="SALE",
                direction="OUT",
                quantity=10,
            )

        self.batch.refresh_from_db()

        self.assertEqual(self.batch.available_quantity, 100)
        self.assertEqual(StockMovement.objects.count(), 0)

    def test_audit_record_created(self):
        apply_stock_movement(
            batch_id=self.batch.id,
            movement_type="SALE",
            direction="OUT",
            quantity=10,
            reference="TEST-SALE-001",
            notes="Automated test sale",
        )

        movement = StockMovement.objects.get(
            reference="TEST-SALE-001"
        )

        self.assertEqual(movement.quantity, 10)
        self.assertEqual(movement.quantity_before, 100)
        self.assertEqual(movement.quantity_after, 90)
