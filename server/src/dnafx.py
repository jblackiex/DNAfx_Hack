import logging
import traceback
from ENV import ENV
from channel_manager import ChannelManager

def main():
    try:
        ENV.init_config()
        IOhub = ChannelManager()
        # IOhub.start_re  
        # pianoferie = PianoFerie()
        # pianoferie.download_sheet_if_changed()
        # if pianoferie.sheet_is_changed:
        #     monthprocessor = MonthProcessor()
        #     monthprocessor.process_this_month()
        #     FILEditor.set_output_statino_file()
        #     FILEditor.set_users_last_work_day_in_file()
        # STATNPayload.send_email_if_month_last_day()
    except Exception as e:
        raise e

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_str = f"Si è verificato un errore: {str(e)}" 
        print(error_str)
        logging.error(traceback.format_exc())
        exit(1)
