"""Integration tests for payment processing service."""

import pytest
from unittest.mock import patch

from payment_service.payment_processor import (
    PaymentProcessor, 
    PaymentStatus, 
    InvalidPaymentError
)


class TestPaymentProcessingIntegration:
    """Integration tests for the payment processing workflow."""
    
    def test_full_payment_workflow(self, payment_processor):
        """Test complete payment workflow: create -> verify -> refund."""
        # Create payment
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = payment_processor.process_payment(
                amount=99.99,
                currency="USD",
                payment_method="card"
            )
        
        # Verify payment was created
        payment = payment_processor.get_payment(payment_id)
        assert payment is not None
        assert payment["amount"] == 99.99
        assert payment["currency"] == "USD"
        assert payment["status"] == PaymentStatus.COMPLETED.value
        
        # Process refund
        result = payment_processor.refund_payment(payment_id)
        assert result is True
        
        # Verify refund status
        status = payment_processor.get_payment_status(payment_id)
        assert status == PaymentStatus.REFUNDED.value
    
    def test_concurrent_payments(self, payment_processor):
        """Test processing multiple payments concurrently."""
        payment_configs = [
            {"amount": 25.00, "currency": "USD"},
            {"amount": 50.00, "currency": "EUR"},
            {"amount": 75.00, "currency": "GBP"},
        ]
        
        payment_ids = []
        
        # Process all payments
        with patch('random.random', return_value=0.5):  # Force success
            for config in payment_configs:
                payment_id = payment_processor.process_payment(**config)
                payment_ids.append(payment_id)
        
        # Verify all payments
        for i, payment_id in enumerate(payment_ids):
            payment = payment_processor.get_payment(payment_id)
            assert payment is not None
            assert payment["amount"] == payment_configs[i]["amount"]
            assert payment["currency"] == payment_configs[i]["currency"]
            assert payment["status"] == PaymentStatus.COMPLETED.value
    
    def test_payment_failure_handling(self, payment_processor):
        """Test handling of payment failures."""
        with patch('random.random', return_value=0.98):  # Force failure
            payment_id = payment_processor.process_payment(amount=10.00)
        
        # Verify payment failed
        status = payment_processor.get_payment_status(payment_id)
        assert status == PaymentStatus.FAILED.value
        
        # Verify refund is not allowed for failed payments
        result = payment_processor.refund_payment(payment_id)
        assert result is False
    
    def test_error_handling_workflow(self, payment_processor):
        """Test error handling in payment processing."""
        # Test invalid amount
        with pytest.raises(InvalidPaymentError, match="Amount must be positive"):
            payment_processor.process_payment(amount=-50.00)
        
        # Test invalid currency
        with pytest.raises(InvalidPaymentError, match="Currency must be 3-letter code"):
            payment_processor.process_payment(amount=50.00, currency="US")
    
    def test_payment_data_integrity(self, payment_processor):
        """Test that payment data maintains integrity throughout processing."""
        original_amount = 123.45
        original_currency = "JPY"
        
        with patch('random.random', return_value=0.5):  # Force success
            payment_id = payment_processor.process_payment(
                amount=original_amount,
                currency=original_currency
            )
        
        # Retrieve payment multiple times to ensure data consistency
        for _ in range(3):
            payment = payment_processor.get_payment(payment_id)
            assert payment["amount"] == original_amount
            assert payment["currency"] == original_currency
            assert payment["id"] == payment_id
