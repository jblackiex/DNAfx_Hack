SUDO=sudo

CC = venv/bin/python3
DIR = src/
PYTEST = PYTHONPATH=${DIR} venv/bin/pytest

# Styling
BOLD = \033[1m
END = \033[0m
RED = \033[91m
GREEN = \033[92m
YELLOW = \033[93m


DNAfx: .venv
	@echo "${GREEN}DNAfx${END}"
	$(SUDO) python3 src/midi_change.py

.venv:
	@if [ ! -d "venv" ]; then python3 -m venv venv; \
		echo "${BOLD}${GREEN}Creating virtual environment..${END}"; \
		venv/bin/pip install -r requirements.txt; \
	fi





# DNAfx_extract_from_loop_wav:
# 	@echo "${GREEN}DNAfx -> extract loop${END}"
# 	$(SUDO) python3 src/extract_from_loop_wav.py

# DNAfx_play:
# 	@echo "${GREEN}DNAfx -> play audio${END}"
# 	$(SUDO) python3 src/play_AUX.py

find_bus:
	@echo "${GREEN}Finding USB devices${END}"
	@echo "${YELLOW} You Must create a VENDOR_ID && PRODUCT_ID variable in .env file and assign values:${END}"
	@echo "${YELLOW}  Example: VENDOR_ID=0483 && PRODUCT_ID=5703${END}"
	$(SUDO) lsusb

find_bus_verbose:
	@echo "${GREEN}Finding USB devices${END}"
	@echo "${YELLOW} You Must create a VENDOR_ID && PRODUCT_ID variable in .env file and assign values:${END}"
	@echo "${YELLOW}  Example: VENDOR_ID=0483 && PRODUCT_ID=5703${END}"
	$(SUDO) lsusb -v

# DNAfx_hid_dump_descriptor:
# 	@echo "${GREEN}Dumping HID descriptor${END}"
# 	$(SUDO) usbhid-dump -d 0483:5703 -e descriptor

# DNAfx_sniff:
# 	@echo "${GREEN}Sniffing USB device${END}"
# 	$(SUDO) modprobe usbmon
# 	$(SUDO) tcpdump -i usbmon1 -w usb_traffic.pcap

# DNAfx_analyze_sniff:
# 	@echo "${GREEN}Sniffing USB device${END}"
# 	$(SUDO) tshark -r usb_traffic.pcap -Y "usb.device_address == 24 && usb.endpoint_address == 0x02" -T fields -e usb.capdata

 