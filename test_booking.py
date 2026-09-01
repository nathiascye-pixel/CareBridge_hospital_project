import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
# Import the function from your file (assuming it's named appointment_system.py)
from book_appointment import book_appointment


class TestBookAppointment(unittest.TestCase):

    @patch("builtins.input")
    @patch("builtins.print")
    def test_valid_gp_booking(self, mock_print, mock_input):
        """Test a successful booking for GP with a valid future date."""
        # Setup input sequence: GP department, date 10 days in the future
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        mock_input.side_effect = ["GP", future_date]

        book_appointment()

        # Assert confirmation message was printed
        mock_print.assert_called_with("Booking is confirmed")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_valid_specialist_booking(self, mock_print, mock_input):
        """Test a successful booking for Specialist with a valid future date."""
        future_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        mock_input.side_effect = ["Specialist", future_date]

        book_appointment()

        mock_print.assert_called_with("Booking is confirmed")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_department_retry(self, mock_print, mock_input):
        """Test recovery from invalid department inputs."""
        future_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        # First enters 'Pharmacy' (invalid), then 'GP' (valid), then valid date
        mock_input.side_effect = ["Pharmacy", "GP", future_date]

        book_appointment()

        # Check that error print occurred
        mock_print.assert_any_call("Invalid Department staff please try again")
        mock_print.assert_called_with("Booking is confirmed")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_date_within_seven_days_rejected(self, mock_print, mock_input):
        """Test that dates 7 days or less from today are rejected."""
        too_soon_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        valid_date = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        # First enters too-soon date, then a valid date
        mock_input.side_effect = ["GP", too_soon_date, valid_date]

        book_appointment()

        mock_print.assert_any_call("Invalid Date please try again")
        mock_print.assert_called_with("Booking is confirmed")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_date_format_rejected(self, mock_print, mock_input):
        """Test that non-date text inputs are rejected."""
        valid_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

        # First enters text instead of date, then valid date
        mock_input.side_effect = ["GP", "not-a-date", valid_date]

        book_appointment()

        mock_print.assert_any_call("Invalid Date please try again")
        mock_print.assert_called_with("Booking is confirmed")


if __name__ == "__main__":
    unittest.main()