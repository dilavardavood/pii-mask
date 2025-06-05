from app.services.llm_service import ask_openai
from app.utils.helper import load_json_from_file, extract_json
from app.utils.prompt_gallery import ministry_identify_prompt, ministry_user_prompt, department_identify_prompt, \
    department_identify_prompt_telegram


def register_grievance(user_query):

    ministry_data = load_json_from_file("Ministry", "main_category")
    ministry_prompt = ministry_identify_prompt(ministry_data)
    user_prompt = ministry_user_prompt(user_query)
    main_ministry = ask_openai(ministry_prompt, user_prompt, temperature=0.0)
    ministry = extract_json(main_ministry)
    detected_ministry = ministry["ministry_key"]
    dept_data = load_json_from_file("Department", detected_ministry)
    dept_prompt = department_identify_prompt(dept_data)
    department = ask_openai(dept_prompt, user_query, temperature=0.0)
    department = extract_json(department)
    return {
        "message": "AI generated data, please verify and submit.",
        "department": department
    }


def handle_grievance(user_query):

    ministry_data = load_json_from_file("Ministry", "main_category")
    ministry_prompt = ministry_identify_prompt(ministry_data)
    user_prompt = ministry_user_prompt(user_query)
    main_ministry = ask_openai(ministry_prompt, user_prompt, temperature=0.0)
    ministry = extract_json(main_ministry)
    print("Main Ministry Response:", ministry)
    detected_ministry = ministry["ministry_key"]
    print("Detected Ministry Key:", detected_ministry)
    dept_data = load_json_from_file("Department", detected_ministry)
    dept_prompt = department_identify_prompt_telegram(dept_data)
    print("Department Prompt:", dept_prompt)
    department = ask_openai(dept_prompt, user_query, temperature=0.0)


    return department