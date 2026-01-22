"""Payment processing service implementation."""

import uuid
from datetime import datetime
from typing import Dict, Optional
from enum import Enum


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentError(Exception):
    """Base payment processing exception."""
    pass


class InvalidPaymentError(PaymentError):
    """Raised when payment data is invalid."""
    pass


class PaymentProcessor:
    """Core payment processing service."""
    
    def __init__(self):
        """Initialize the payment processor."""
        self._payments: Dict[str, dict] = {}
    
    def process_payment(self, amount: float, currency: str = "USD", 
                         payment_method: str = "card") -> str:
        """
        Process a payment.
        
        Args:
            amount: Payment amount
            currency: Currency code (default: USD)
            payment_method: Payment method (default: card)
            
        Returns:
            Payment ID
            
        Raises:
            InvalidPaymentError: If payment data is invalid
        """
        if amount <= 0:
            raise InvalidPaymentError("Amount must be positive")
        
        if not currency or len(currency) != 3:
            raise InvalidPaymentError("Currency must be 3-letter code")
        
        payment_id = str(uuid.uuid4())
        
        payment_data = {
            "id": payment_id,
            "amount": amount,
            "currency": currency.upper(),
            "payment_method": payment_method,
            "status": PaymentStatus.PENDING.value,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        self._payments[payment_id] = payment_data
        
        # Simulate payment processing
        self._update_payment_status(payment_id, PaymentStatus.PROCESSING)
        
        # Simulate success/failure (95% success rate)
        import random
        if random.random() < 0.95:
            self._update_payment_status(payment_id, PaymentStatus.COMPLETED)
        else:
            self._update_payment_status(payment_id, PaymentStatus.FAILED)
        
        return payment_id
    
    def get_payment(self, payment_id: str) -> Optional[dict]:
        """
        Get payment details.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment data or None if not found
        """
        return self._payments.get(payment_id)
    
    def refund_payment(self, payment_id: str) -> bool:
        """
        Refund a payment.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            True if refund successful, False otherwise
        """
        payment = self._payments.get(payment_id)
        if not payment:
            return False
        
        if payment["status"] != PaymentStatus.COMPLETED.value:
            return False
        
        self._update_payment_status(payment_id, PaymentStatus.REFUNDED)
        return True
    
    def _update_payment_status(self, payment_id: str, status: PaymentStatus):
        """Update payment status."""
        if payment_id in self._payments:
            self._payments[payment_id]["status"] = status.value
            self._payments[payment_id]["updated_at"] = datetime.utcnow().isoformat()
    
    def get_payment_status(self, payment_id: str) -> Optional[str]:
        """
        Get payment status.
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment status or None if not found
        """
        payment = self._payments.get(payment_id)
        return payment["status"] if payment else None
