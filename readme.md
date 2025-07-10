# Signup API 

Signup API with fields: name, email, designation, district, state, password, confirm password

OTP-based Email Verification (using an open-source protocol like SMTP)

User is only created after OTP verification

# OTP Verification API
1 Accept user's email and entered OTP
2 Check if it matches the latest OTP for that email
3 If valid:
  Mark the user as active
  Delete the OTP record (optional)
4 Return success response






















