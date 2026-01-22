"""Unit tests for payment processor."""

import unittest
from unittest.mock import patch
from datetime import datetime

from payment_service.payment_processor import (
    PaymentProcessor, 
    PaymentStatus, 
    InvalidPaymentError
)


class TestPaymentProcessor(unittest.TestCase):
    """Test cases for PaymentProcessor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = PaymentProcessor()
    
    def test_process_payment_success(self):
        """Test successful payment processing."""
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = self.processor.process_payment(
                amount=100.00, 
                currency="USD", 
                payment_method="card"
            )
            
            self.assertIsNotNone(payment_id)
            payment = self.processor.get_payment(payment_id)
            self.assertIsNotNone(payment)
            self.assertEqual(payment["amount"], 100.00)
            self.assertEqual(payment["currency"], "USD")
            self.assertEqual(payment["payment_method"], "card")
    
    def test_process_payment_invalid_amount(self):
        """Test payment processing with invalid amount."""
        with self.assertRaises(InvalidPaymentError):
            self.processor.process_payment(amount=-10.00)
        
        with self.assertRaises(InvalidPaymentError):
            self.processor.process_payment(amount=0)
    
    def test_process_payment_invalid_currency(self):
        """Test payment processing with invalid currency."""
        with self.assertRaises(InvalidPaymentError):
            self.processor.process_payment(amount=100.00, currency="US")
        
        with self.assertRaises(InvalidPaymentError):
            self.processor.process_payment(amount=100.00, currency="")
    
    def test_get_payment_not_found(self):
        """Test getting non-existent payment."""
        result = self.processor.get_payment("non-existent-id")
        self.assertIsNone(result)
    
    def test_get_payment_status(self):
        """Test getting payment status."""
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = self.processor.process_payment(amount=50.00)
            status = self.processor.get_payment_status(payment_id)
            self.assertEqual(status, PaymentStatus.COMPLETED.value)
    
    def test_get_payment_status_not_found(self):
        """Test getting status of non-existent payment."""
        status = self.processor.get_payment_status("non-existent-id")
        self.assertIsNone(status)
    
    def test_refund_payment_success(self):
        """Test successful payment refund."""
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = self.processor.process_payment(amount=75.00)
            
            # Verify payment is completed
            payment = self.processor.get_payment(payment_id)
            self.assertEqual(payment["status"], PaymentStatus.COMPLETED.value)
            
            # Test refund
            result = self.processor.refund_payment(payment_id)
            self.assertTrue(result)
            
            # Verify status changed to refunded
            status = self.processor.get_payment_status(payment_id)
            self.assertEqual(status, PaymentStatus.REFUNDED.value)
    
    def test_refund_payment_not_found(self):
        """Test refunding non-existent payment."""
        result = self.processor.refund_payment("non-existent-id")
        self.assertFalse(result)
    
    def test_refund_payment_not_completed(self):
        """Test refunding payment that is not completed."""
        # Create a payment that will fail
        with patch('random.random', return_value=0.98):  # Force failure
            payment_id = self.processor.process_payment(amount=25.00)
            
            # Verify payment failed
            status = self.processor.get_payment_status(payment_id)
            self.assertEqual(status, PaymentStatus.FAILED.value)
            
            # Try to refund failed payment
            result = self.processor.refund_payment(payment_id)
            self.assertFalse(result)
    
    def test_payment_currency_normalization(self):
        """Test that currency is properly normalized to uppercase."""
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = self.processor.process_payment(
                amount=100.00, 
                currency="eur"  # lowercase
            )
            
            payment = self.processor.get_payment(payment_id)
            self.assertEqual(payment["currency"], "EUR")
    
    def test_payment_timestamps(self):
        """Test that payment timestamps are properly set."""
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = self.processor.process_payment(amount=30.00)
            
            payment = self.processor.get_payment(payment_id)
            self.assertIn("created_at", payment)
            self.assertIn("updated_at", payment)
            
            # Verify timestamps are valid ISO format
            created_at = datetime.fromisoformat(payment["created_at"])
            updated_at = datetime.fromisoformat(payment["updated_at"])
            self.assertIsNotNone(created_at)
            self.assertIsNotNone(updated_at)
    
    def test_multiple_payments(self):
        """Test processing multiple payments."""
        payment_ids = []
        
        with patch('random.random', return_value=0.5):  # Force success
            for i in range(3):
                payment_id = self.processor.process_payment(
                    amount=float(10 * (i + 1))
                )
                payment_ids.append(payment_id)
        
        # Verify all payments exist and have correct amounts
        for i, payment_id in enumerate(payment_ids):
            payment = self.processor.get_payment(payment_id)
            self.assertIsNotNone(payment)
            self.assertEqual(payment["amount"], float(10 * (i + 1)))


if __name__ == '__main__':
    unittest.main()
