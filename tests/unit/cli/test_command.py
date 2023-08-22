# import os

# from darkwebiq.cli.command import file_to_text
# from darkwebiq.commons import logger


# def test_files_to_text() -> None:
#     dir = os.getenv("TEST_UNZIPPED_FILES")
#     out_file = os.getenv("TEST_UNZIPPED_FILES_OUT_FILE")
#     if out_file:
#         if dir is None or out_file is None:
#             raise Exception(
#                 "TEST_UNZIPPED_FILES or TEST_UNZIPPED_FILES_OUT_FILE is not defined."
#             )
#         file_to_text(dir, out_file)
#     else:
#         logger.warning(f"No TEST_UNZIPPED_FILES defined.")
