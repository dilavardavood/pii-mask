def get_pii_prompt(strictness="MEDIUM", mask_entity=None):
    if mask_entity is None:
        mask_entity = ["name", "phone", "email", "aadhaar", "PAN", "address", "dob"]

    entities_string = ", ".join(mask_entity)

    strictness_instructions = {
        "HIGH": """
Completely mask the specified entities with no identifiable hints. Replace all characters with asterisks. Example:
- "Rajeev" → "******"
- "9876543210" → "**********"
- "ravi.kumar@gmail.com" → "***********************"
""",
        "MEDIUM": """
Apply strict masking. Retain only minimal hints (such as the first or last character) while masking all other characters.
Examples:
- "Rajeev" → "R*****"
- "9876543210" → "********10"
- "ravi.kumar@gmail.com" → "r***@g****.com"
""",
        "LOW": """
Apply moderate masking. Preserve partial structure or syllables where possible, while ensuring no exact PII is exposed.
Examples:
- "Rajeev Sinha" → "R**** S****"
- "9876543210" → "98******10"
- "ravi.kumar@gmail.com" → "ra***.ku***@gma**.com"
"""
    }

    pii_prompt = f"""
You are a data anonymization engine. Your task is to receive JSON data from various sources and mask Personally Identifiable Information (PII).

Input:
- A JSON object from a CSO source. The structure may vary.
- The fields to mask are: {entities_string}.
- Masking strictness level: {strictness.upper()}.

Instructions:
- Detect and mask the fields listed above, wherever they occur in the JSON (including nested objects).
- {strictness_instructions.get(strictness.upper(), strictness_instructions["MEDIUM"]).strip()}
- Maintain the original JSON structure and keys.
- Do not mask non-PII fields like status, IDs, timestamps, etc.
- Use asterisks (*) for masking only.
- Return only the updated JSON with masked PII.

Examples:
"email": "ravi.kumar@gmail.com" → "r***@g****.com"  
"aadhaar": "1234-5678-9012" → "****-****-9012"  
"dob": "1990-05-14" → "1990-**-**"
"""
    return pii_prompt.strip()

#
# def get_pii_substitution_prompt(strictness="MEDIUM", entity=None):
#
#     mask_entity = ["name", "phone", "email", "aadhaar", "PAN", "address", "dob"].append(entity)
#
#     entities_string = ", ".join(mask_entity)
#
#     strictness_instructions = {
#         "HIGH": """
# Replace all specified PII fields with fully synthetic values that resemble the original type, format, and structure — but contain no real user-identifiable information.
# Examples:
# - Names: "Rajeev Sinha" → "Arjun Verma"
# - Email: "rajeev.sinha@gmail.com" → "random.user123@demo.com"
# - Aadhaar: "1234-5678-9012" → "0000-1111-2222"
# - Date of Birth: "1990-05-14" → "1980-01-01"
# """,
#         "MEDIUM": """
# Substitute PII fields with partially obfuscated but still synthetic values. Preserve some real structure, like domain names or city names.
# Examples:
# - Email: "rajeev.sinha@gmail.com" → "test.user@gmail.com"
# - Address: "123 MG Road, Bangalore" → "456 Park Ave, Bangalore"
# - Name: "Anita Sharma" → "Neha Kapoor"
# """,
#         "LOW": """
# Use light substitution — modify only identifiable parts of the value while retaining its usability for demo or internal purposes.
# Examples:
# - Phone: "9876543210" → "9000000000"
# - Email: "a.sharma@example.com" → "user@example.com"
# - Name: "Amit" → "Amit (Test)"
# """
#     }
#
#     substitution_prompt = f"""
# You are a data anonymization engine. Your task is to receive JSON data from various sources and substitute all Personally Identifiable Information (PII) with dummy but valid-looking values.
#
# Input:
# - A JSON object from a CSO source. The structure may vary.
# - Fields to substitute: {entities_string}.
# - Substitution strictness level: {strictness.upper()}.
#
# Instructions:
# - Identify all occurrences of the above-listed PII fields in the JSON, even if deeply nested.
# - {strictness_instructions.get(strictness.upper(), strictness_instructions["MEDIUM"]).strip()}
# - Keep the JSON structure, key names, and formatting unchanged.
# - Use realistic fake values — not masking with asterisks.
# - Ensure consistent replacement (e.g., same name reused in different places should use the same dummy name).
#
# Return only the updated JSON with substituted dummy values.
#
# Examples:
# "email": "ravi.kumar@gmail.com" → "john.doe@testmail.com"
# "aadhaar": "1234-5678-9012" → "1111-2222-3333"
# "dob": "1990-05-14" → "1980-01-01"
# """
#     return substitution_prompt.strip()


def get_pii_substitution_prompt(strictness="MEDIUM", entity=None):
    if entity is None:
        entity = []

    mask_entity = ["name", "phone", "email", "aadhaar", "PAN", "address", "dob"] + entity
    entities_string = ", ".join(mask_entity)

    strictness_instructions = {
        "HIGH": """
Replace all specified PII fields with fully synthetic values that resemble the original type, format, and structure — but contain no real user-identifiable information. 
Examples:
- Names: "Rajeev Sinha" → "Arjun Verma"
- Email: "rajeev.sinha@gmail.com" → "random.user123@demo.com"
- Aadhaar: "1234-5678-9012" → "0000-1111-2222"
- Date of Birth: "1990-05-14" → "1980-01-01"
""",
        "MEDIUM": """
Substitute PII fields with partially obfuscated but still synthetic values. Preserve some real structure, like domain names or city names.
Examples:
- Email: "rajeev.sinha@gmail.com" → "test.user@gmail.com"
- Address: "123 MG Road, Bangalore" → "456 Sample Street, Bangalore"
- Name: "Anita Sharma" → "Neha Kapoor"
""",
        "LOW": """
Use light substitution — modify only identifiable parts of the value while retaining its usability for demo or internal purposes.
Examples:
- Phone: "9876543210" → "9000000000"
- Email: "a.sharma@example.com" → "user@example.com"
- Name: "Amit" → "Amit (Test)"
"""
    }

    substitution_prompt = f"""
You are a data anonymization engine. Your task is to receive JSON data from various sources and substitute all Personally Identifiable Information (PII) with realistic-looking dummy values.

Input:
- A JSON object from a CSO source. The structure may vary.
- Fields to substitute: {entities_string}.
- Substitution strictness level: {strictness.upper()}.

Instructions:
- Identify all occurrences of the above-listed PII fields in the JSON, including nested ones.
- {strictness_instructions.get(strictness.upper(), strictness_instructions["MEDIUM"]).strip()}
- Maintain the **exact original JSON structure and key names**.
- DO NOT change geographic or location-specific context (e.g., keep city, state, pin code, and landmarks intact in addresses or descriptions).
- For example:
  - Address: "123 MG Road, Bangalore" → "456 Sample Street, Bangalore" ✅ (city retained)
  - Description: "...from MG Road, Pune" → "...from Sample Street, Pune" ✅
- Reuse the same dummy value if the same PII is repeated in multiple fields.
- Do not use asterisks or masking — only substitution with consistent and realistic values.

Return only the updated JSON with PII substituted according to these rules.
"""
    return substitution_prompt.strip()
