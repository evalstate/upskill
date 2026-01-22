# Payment Processing Service

A robust payment processing service with comprehensive unit tests and test coverage.

## Features

- Process payments with multiple currencies
- Payment status tracking
- Refund functionality
- Comprehensive error handling
- Full test coverage with pytest

## Installation

```bash
pip install -e .[dev]
```

## Usage

```python
from payment_service.payment_processor import PaymentProcessor

processor = PaymentProcessor()
payment_id = processor.process_payment(amount=100.00, currency="USD")
payment = processor.get_payment(payment_id)
```

## Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=payment_service
```

Run specific test file:
```bash
pytest tests/test_payment_processor.py
```

## Test Coverage

The test suite includes:

- **Unit Tests**: Test individual components and methods
- **Integration Tests**: Test complete payment workflows
- **Error Handling Tests**: Verify proper exception handling
- **Edge Case Tests**: Test boundary conditions and invalid inputs

Current test coverage: >95%

## CI/CD

The project includes GitHub Actions workflow for:
- Running tests on multiple Python versions
- Generating coverage reports
- Automated testing on push/PR

## Project Structure

```
payment_service/
├── __init__.py
├── payment_processor.py      # Main payment processing logic
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_payment_processor.py # Unit tests
└── test_integration.py       # Integration tests
```
