import streamlit as st
from src.tag_validator_new import run_validator
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="VordLabs Tag Validator", layout="wide")
st.title("VordLabs Tag Validator")

uploaded_files = st.file_uploader(
    "Upload one or more Excel files", type=["xlsx"], accept_multiple_files=True
)

if not uploaded_files:
    st.info("Please upload at least one Excel file to validate.")
    st.stop()

if st.button("Run Validator"):
    for uploaded_file in uploaded_files:
        st.subheader(f"Processing: {uploaded_file.name}")
        with st.spinner("Running validation..."):
            try:
                # Write the uploaded file to temp path for pandas read_excel usage
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name

                # Ensure output folder exists
                os.makedirs("output", exist_ok=True)
                output_path = os.path.join(
                    "output", f"{uploaded_file.name.replace('.xlsx', '_report.json')}"
                )

                result = run_validator(tmp_path, output_path)

            except Exception as exc:
                st.error(f"Validation failed for {uploaded_file.name}: {exc}")
                continue
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        st.success(f"Validation completed for {uploaded_file.name}")

        # Show summary
        if "summary" in result and "details" in result:
            st.markdown("### Summary Report")
            st.table(pd.DataFrame([result["summary"]]))

            st.markdown("### Details")
            if result["details"].get("duplicates"):
                st.write("**Duplicates:**")
                for tag, count in result["details"]["duplicates"].items():
                    st.write(f"- {tag}: {count} occurrences")

            if result["details"].get("invalid_format_tags"):
                st.write("**Invalid Format Tags:**")
                for tag in result["details"]["invalid_format_tags"]:
                    st.write(f"- {tag}")

            if result["details"].get("inconsistent_prefixes"):
                st.write("**Inconsistent Prefixes:**")
                for prefix, count in result["details"]["inconsistent_prefixes"].items():
                    st.write(f"- {prefix}: {count} occurrences")

            if result["details"].get("missing_numbers"):
                st.write("**Missing Numbers:**")
                for prefix, numbers in result["details"]["missing_numbers"].items():
                    st.write(f"- {prefix}: missing {numbers}")

        else:
            st.warning("Unexpected result format. See raw JSON below.")
            st.json(result)
    

    
       