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
            
            st.subheader("Duplicate Tags")

            duplicates = result["details"]["duplicates"]

            if duplicates:
                dup_df = pd.DataFrame(list(duplicates.items()), columns=["Tag", "Count"])
                st.dataframe(dup_df)
            else:
                st.write("No duplicates found")

            st.subheader("Invalid Format Tags")

            invalid_formats = result["details"]["invalid_format_tags"]

            if invalid_formats:
                st.dataframe(pd.DataFrame(invalid_formats, columns=["Invalid Tags"]))
            else:
                st.write("None")
           
            # st.subheader("Inconsistent Prefixes")

            # invalid_prefix = result["details"]["inconsistent_prefixes"]

            # if invalid_prefix:
            #     st.dataframe(pd.DataFrame(invalid_prefix, columns=["Tags"]))
            # else:
            #     st.write("None")
                
            
            st.subheader("Missing Numbers")

            missing = result["details"]["missing_numbers"]

            if missing:
                for prefix, nums in missing.items():
                    st.dataframe(pd.DataFrame(nums, columns=[f"Missing Numbers for {prefix}"]))
                    # st.write(f"{prefix}: {nums}")
            else:
                st.write("No missing numbers")
            
            
            st.subheader("Inconsistent Prefix Counts")
            inconsistent_prefixes = result["details"]["inconsistent_prefixes"]
            if inconsistent_prefixes:
                prefix_counts = pd.DataFrame(list(inconsistent_prefixes.items()), columns=["Prefix", "Count"])
                st.dataframe(prefix_counts)
            else:
                st.write("No inconsistent prefixes found")

            
            st.success("Validation Completed Successfully!")

        else:
            st.warning("Unexpected result format. See raw JSON below.")
            st.json(result)
    

    
       