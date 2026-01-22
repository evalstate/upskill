"""Test configuration and fixtures."""

import pytest
from payment_service.payment_processor import PaymentProcessor


@pytest.fixture
def payment_processor():
    """Create a fresh payment processor instance for testing."""
    return PaymentProcessor()


@pytest.fixture
def mock_success_payment():
    """Mock payment data for successful payment."""
    return {
        "amount": 100.00,
        "currency": "USD",
        "payment_method": "card"
    }
