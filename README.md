# DNAfx_Hack

`Dnafx_Hack` is an open source project designed for the Harley Benton DNAfx GiT series of guitar pedals:

- DNAfx GiT (TESTED!)
- DNAfx GiT Core (untested)
- DNAfx GiT Advanced (untested)

I wanted to switch presets on my DNAfx GiT guitar pedal via PC but unfortunately I have Linux. Harley Benton gives you a decent Windows program but I have Linux (again) AND it doesn’t allow you to control Tuner and Looper functionalities; AND I also wanted to import previous recorded looper audio tracks into the Looper: If you are jamming on a “just recorded” cool looper track and electricity goes off, you lost your track forever as the pedal doesn’t store audio tracks in memory and you won’t be able to jam again on that recording.

No useful github repos found, no knowledge on how DNAfx protocol works.

I connected DNAfx to my PC via USB, and with the help of Wireshark and the original Windows program, I sniffed all the presets, then created a **`server/`** that allows you to switch preset typing the wanted preset with keyboard, or remotely via raw socket throught a custom Android App, the **`client/`** side.

At that point I could go back and forth or to “42” or “Rockk-preset” just by clicking a button on my smartphone, simple as that. BUT, as I said, I wanted to being able to control Tuner and, most importantly, the Looper functionality. Unfortunately you cannot send a payload to pedal via USB that triggers Looper or Tuner, so, I ended up building an external circuit to simulate button presses electronically, allowing me to control those two physical buttons via software instead of pressing them by hand or foot. Thanks to that, I unlocked a **`new functionality`**: **the ability to import previously recorded tracks into the looper mode** of the DNAfx GiT pedal.

This means that instead of starting from scratch every time, I can now **load older loop recordings,** saved externally, directly into the pedal's looper buffer. This is particularly useful for live performances or rehearsals where I want to reuse a backing loop or a complex layered part without having to recreate it on the spot.

Here's what this **`new functionality`** enables:

- 🎛 Seamless integration with the existing looper workflow: imported tracks behave just like freshly recorded ones, with near-identical performance and responsiveness.
- 💾 **Storage flexibility**: tracks can be prepared and saved externally (e.g. on the Android app or Raspberry Pi), then imported on demand.
- 📲 **Remote control support**: using the Android app and the client-server architecture I've built, you can trigger the import remotely.
- 🔁 **Creative freedom**: build a library of loops and call them up as needed, opening up more complex live or studio applications.

If you choose to [create the external circuit](#how-it-works) you're basically turning the looper into a **preset system for loops**, which is a huge step forward in functionality:

- You can **prepare loops ahead of time** (like presets)
- Store them externally (on Raspberry Pi)
- And **load/import them on demand**, just like you'd load a sound preset on a synth or amp.

## 📜 Index

- [**How it works? ⚙️**](#how-it-works)
- [**How to Build the External Circuit ⚡🔌**](#how-to-build-the-external-circuit-)
- [**Setup and Run 🛠️ 🏃🏼‍♂️**](#setup-and-run)
- [**Environment Configuration (.env file) 🧭**](#environment-configuration-env-file-)
- [**Running ✅**](#running-)
- [**Contributing 🤝**](#contributing-)
- [**Other DNAfx-related project 🧩**](#other-dnafx-related-project-)
- [**Disclaimer ⚠️**](#disclaimer)



---
<a name="how-it-works"></a>
## How it works? ⚙️

![DNAfx_Hack.svg](DNAfx_Hack%201b831ef5b6c7809baa76c494069a73df/DNAfx_Hack.svg)

(CLICK the diagram to open it full screen and zoom in)

I put **`server/`** on my Raspberry Pi and with `make` I run a python script that start listening for keyboard inputs and socket data. As long as your Raspberry Pi and mobile device are on the same network, just retrieve the Raspberry Pi's IP address and use it to connect via the `Dnafx Android` app.

The app is very simple: tap “+” to create a new string command (available commands are listed below), and use “prev” and “next” to switch presets. You can connect your Raspberry Pi to the network either via Ethernet or a Wi-Fi adapter (see the SVG diagram above). If you're using a Wi-Fi adapter, make sure to install the necessary drivers.

Once that's done, set up the script to start automatically when the Raspberry Pi boots. At that point, you can type something on the keyboard *and* send a string via socket at the same time, `asyncio` will handle everything smoothly.

- **Sending via USBHID**: you type with keyboard or send “0” with **`client/`** Android app, the script will use “0” as the key of a dictionary to get the payload value (the command that allows you to switch preset) and send it to the pedal through **USBHID Channel.** You can find all preset commands in `server/config/presets.json`.
    
    
    | **Command Format** | **Description** | **Example Input** | **Behavior** |
    | --- | --- | --- | --- |
    | `""` (empty string) | Moves to the next preset. If the last preset is `199`, it resets to `0`. | `""` | Moves forward by 1 preset. Resets to `0` if at `199`. |
    | `"-"` | Moves to the previous preset. If at `0`, wraps around to `200`. | `"-"` | Moves back by 1 preset (`last_preset - 1`). If at `0`, jumps to `200`. |
    | **Preset Addition** (`<name>_add<pos>`) | Adds a new preset with a name at the specified position. | `"CoolEffect_add150"` | Copies the value of preset  `"150"` in `config/presets.json`to the new name `"CoolEffect"` at updating JSON file. |
    | **Preset Name** | Sends a preset by name if it exists in the list. | `"FLANGER"` | Finds `"FLANGER"` in `config/presets.json` and sends its corresponding USB command (value). |
    | **Preset Index (Number)** | Sends a preset by numerical index. Must be in range. | `"15"` | Sends the preset stored at index `15-1` (`14` in the JSON file) |
    | **Invalid Input** | If the input is not a number or valid preset name, it shows an error. | `"15ab"` | Prints `"Invalid input. Please enter a valid effect index/name."` |
    | **USB Command Sending** | Every valid preset is sent twice to respect a 2ms interval. | `"CHORUS"` | Sends `"CHORUS"`'s corresponding command via USB HID. |

---

## How to Build the External Circuit ⚡🔌

*(a.k.a. Unlocking the Tuner + New Looper Import Mode)*

To view the full schematic, CLICK here: [**DNAfx_Hack.svg**.](https://lucid.app/lucidchart/801ec904-747f-40c8-86a8-fbb14ffee57e/view) DO IT!

As shown, the diagram lists all components required to build the external circuit and extend your DNAfx pedal's capabilities.

### ⚠️ Disclaimer

> I'm not a professional electronics engineer — I'm just a passionate developer who's new to electronics. This was my first time designing and building a circuit from scratch, so it may not follow all best practices. I’m not responsible for any potential damage to your device. That said, I tested everything carefully and it works great for my use case. Feedback and suggestions from more experienced makers are always welcome!
> 

### 🔧 Key Concept

A **Raspberry Pi** has been added as the central controller of the system. It communicates with the DNAfx pedal in two ways:

- **Via USB HID** to switch presets programmatically
- **Via GPIO pins** to trigger **relays** that simulate physical button presses (for actions like activating the **Looper** or **Tuner**)

### 🔁 Circuit Logic and Protection

The GPIO pins act as **digital outputs**, each connected to a **BC327 PNP transistor**. These transistors **control the relay coils**, allowing safe activation without stressing the Pi's GPIOs.

Here’s the basic logic:

- GPIO pins are set to **HIGH (3.3V)** by default
- When a pin goes **LOW (0V)**, it **turns on the transistor**
- The transistor then **allows current to flow to the relay**, closing the contact
- The relay simulates a button press by briefly shorting specific points (e.g. yellow to black for the looper, or yellow to red for the tuner)

The transistors are essential because the GPIO pins alone **cannot supply enough current** to drive a relay coil directly. The **BC327s act as current amplifiers**, safely switching the higher current needed.

To **protect the Raspberry Pi**, I calculated the required current and added **base resistors** in front of each transistor. This limits the current drawn from the GPIO pins and prevents potential damage.

---

### 📐 Current Calculation

This section explains how I calculated the appropriate **base resistor** between the Raspberry Pi’s GPIO and the base of a **BC327 PNP transistor**, used to activate a **KY-019 5V relay module** powered at 3.3V.

Even though the relay is rated for 5V, I’m powering it at **3.3V** from the Raspberry Pi. Despite the reduced voltage, it still functions, but we need to carefully calculate the current and protect the GPIO pins. (I checked on relays manual and also 3.3V works)

---

**1️⃣ Relay Coil Current**

The KY-019 relay typically requires **70–100mA** to activate at 5V. Powering it at 3.3V slightly reduces its pull-in current, but to stay safe, we assume:

```
Relay Coil Current (I_C) ≈ 80mA = 0.08A
```

The **BC327** transistor can handle up to **800mA**, so it can safely drive the relay coil.

---

**2️⃣ Required Base Current**

The transistor's current gain (**hFE**) is approximately **100** (conservative value).

Using the formula:

```
I_B = I_C / hFE = 80mA / 100 = 0.8mA
```

This is the amount of current the **GPIO must provide** through the base resistor to turn on the transistor.

---

**3️⃣ Voltage Drop Across the Base Resistor**

The Raspberry Pi GPIO outputs **3.3V**, and the typical base-emitter voltage drop (**V_BE**) of the BC327 is about **0.7V**.

So, the voltage across the base resistor is:

```
V_R = V_GPIO - V_BE = 3.3V - 0.7V = 2.6V
```

---

**4️⃣ Calculating the Base Resistor**

Now we calculate the resistor using Ohm’s Law:

```
R = V_R / I_B = 2.6V / 0.0008A = 3250Ω
```

The closest standard resistor values are:

- **3.3kΩ** (recommended)
- **3kΩ** (if you want to supply a bit more base current for extra margin. I did this.)

Either value will work safely.

---

**5️⃣ GPIO Current Safety**

Using a **3.3kΩ resistor**, the GPIO will supply:

```
I = V / R = 2.6V / 3300Ω ≈ 0.79mA
```

Even if you use a **2.7kΩ resistor**, you’ll only draw:

```
I = 2.6V / 2700Ω ≈ 0.96mA
```

Since Raspberry Pi GPIOs can safely source **up to ~16mA**, these values are well within the safe operating range. So:

✅ The **GPIO pin is protected**

✅ The **transistor receives enough base current to switch reliably**

✅ The **relay activates correctly**

---

### 🧱 Circuit Assembly

The entire circuit is built on a **small breadboard** mounted inside the DNAfx enclosure. This allows for **easy connection *without soldering*** and keeps the system modular for future upgrades.

A **5V fan** is also installed to ensure proper cooling, maintaining stability and preventing overheating during long sessions or high ambient temperatures.

Be sure to use **insulating material** to avoid contact between the Raspberry Pi and DNAfx components; this is crucial for both safety and signal integrity.

### 🎫 Bonus: 3D-Printed Backplate

To make all of this accessible and upgradable, I asked my friend **Pino** to design and 3D-print a **custom back panel** for the DNAfx GiT pedal. This makes it easy to maintain the internal hardware and expand functionalities in the future, without needing to open up or rewire the entire unit.

![image.png](DNAfx_Hack%201b831ef5b6c7809baa76c494069a73df/image.png)

![image.png](DNAfx_Hack%201b831ef5b6c7809baa76c494069a73df/image%201.png)

![image.png](DNAfx_Hack%201b831ef5b6c7809baa76c494069a73df/image%202.png)

![image.png](DNAfx_Hack%201b831ef5b6c7809baa76c494069a73df/image%203.png)

![image.png](DNAfx_Hack%201b831ef5b6c7809baa76c494069a73df/image%204.png)

- **Sending via GPIO:**
    
    
    | **Command Format** | **Description** | **Example Input** | **Behavior** |
    | --- | --- | --- | --- |
    | `"looperMODE"` | Activates **Looper Mode** and clears the current recording. | `"looperMODE"` | Sends a GPIO signal via `GPIO_PIN_NEXT`, waits 1 second, then releases it. |
    | `"auxrecMODE_<file.wav>"` (Only in Looper Mode) | Starts recording, sends the track via AUX, then stops recording. | `"recMODE_rec1.wav"` saves `rec1.wav`  in `./tracks/` | Presses `GPIO_PIN_BACK` to start recording, sends `aux_data` to AUX, then stops recording via `GPIO_PIN_NEXT`. |
    | `"tunerMODE"` | Activates **Tuner Mode** | `"tunerMODE"` | Sends a GPIO signal via `GPIO_PIN_BACK`, waits 1 second, then releases it. |
    | `“playMODE”` | In **Looper Mode**, plays the audio or starts recording if the track is empty.
    If a track is playing and this command is used again, it will start overdubbing 
    on the current track. Outside of Looper Mode, it moves to the previous preset. | `“playMODE”` | Sends a GPIO signal via `GPIO_PIN_BACK`, then releases it. |
    | `“stopMODE”` | In **Looper Mode** stop the audio if you already press play; go to the next preset if not in Looper | `“stopMODE”` | Sends a GPIO signal via `GPIO_PIN_NEXT`, then releases it. |
    | `“otgexpMODE_<filename.wav>_<secondstorec>”` | In **Looper Mode** plays the audio and uses an OTG cable to export it. | `“otgexpMODE_newrec.wav_3”`→ create a new track `./tracks/newrec.wav` 3 seconds long. | Sends a GPIO signal via `GPIO_PIN_BACK`, then releases it, start recording from otg channel, Sends a GPIO signal via `GPIO_PIN_NEXT`, then releases it to stop the track. |
    
    ### **Special Conditions**
    
    - `USE_GPIO` **must be `"ON"` in .env file** for any GPIO-based command to work.
    - `"recMODE"` **only works if** `looperMODE` **is active**.
    - GPIO signals are toggled with `gpioget`, using **pull-down** (press) and **pull-up** (release).
    - `“otgexpMODE_<filename.wav>_<secondstorec>”` **only works** if OTG cable is plugged in.
    - `"auxrecMODE_<file.wav>”` **only works** if AUX cable is plugged in.

You can get the **complete list of available commands** typing `help <command>`  with your keyboard once you execute the script:

```python
def command_help(command):
        """
        Provides a description of the specified command.

        Parameters:
        - command (str): The name of the command to describe.

        Returns:
        - str: Description of the command.

        if command is empty, it will print the list of all commands
        """

        if command == "":
            return "\n\n".join(
            f"{cmd}:\n{desc}" for cmd, desc in command_descriptions.items()
        )
        # Dictionary to hold command descriptions
        command_descriptions = {
            "": "Moves to the next preset. If the last preset is 199, it resets to 0.",
            "-": "Moves to the previous preset. If at 0, wraps around to 200.",
            "preset_add_number": (
                "Adds a new preset with the specified name at the given position. "
                "For example, 'CoolEffect_add150' copies the value of preset 150 "
                "HOW IT WORKS: CoolEffect_add_15 add a 'CoolEffect' preset at position 14 "
            ),
            "preset_name": (
                "Sends a preset by name if it exists in the list. For example, 'FLANGER' "
                "HOW IT WORKS: 'FLANGER' preset and activates it."
            ),
            "preset_index": (
                "Sends a preset by its numerical index. Must be within the valid range. "
                "HOW IT WORKS: '15' activates the preset stored at index 14."
            ),
            "looperMODE": (
                "Activates Looper Mode or clears the current recording. This allows you "
                "to start a new looping session from scratch."
            ),
            "auxrecMODE": (
                "In Looper Mode, starts recording, sends the specified audio file via AUX, "
                "then stops recording. For example, 'auxrecMODE_rec1.wav' records the 'rec1.wav' "
                "file into the looper. The track will be available at './tracks/rec1.wav'."
                "HOW IT WORKS: auxrecMODE_file.wav → import on dnafx track ./tracks/track.wav."
            ),
            "tunerMODE": "Activates Tuner Mode, enabling you to tune your instrument.",
            "playMODE": (
                "In Looper Mode, plays the audio or starts recording if the track is empty. "
                "If a track is playing and this command is used again, it will start overdubbing "
                "on the current track. Outside of Looper Mode, it moves to the previous preset."
            ),
            "stopMODE": (
                "In Looper Mode, stops the audio if it's currently playing. Outside of Looper Mode, "
                "it moves to the next preset."
            ),
            "otgexpMODE": (
                "In Looper Mode, plays the audio and uses an OTG cable to export it. Ensure that "
                "an OTG cable is connected for this function to work properly."
                "HOW IT WORKS: otgexpMODE_newrec.wav_3 → create a new track ./tracks/newrec.wav 3 seconds long."
            ),
        }

        description = command_descriptions.get(command, "Command not found. Please enter a valid command.")
        return description4
```

**If you need an additional input interface**, **like using bluetooth** (see [Pi Zero Bluetooth](https://blog.lminiero.it/pi0w-presenter/?fbclid=PAY2xjawJfNOFleHRuA2FlbQIxMAABpwG1ZwjnOslaYd8kpbVkqNmILpbvqgtQUHoVWpu9klXLu9QSVi1UMl7yJFcA_aem__IGH7WDIXMpb1Etn1CUWYw)) instead of wifi/ethernet connection, just implement the **`InputChannel`** interface, instantiate a new object inside `ChannelManager()` and add a new coroutine here (`dnafx.py`):

```python
async def main():
    try:
        ENV.init_config()
        IOhub = ChannelManager() # ADD BLUETOOTH DOWN HERE ( i.e IOhub.receive_bluetooth() )
        await asyncio.gather(IOhub.receive_socket(), IOhub.receive_keyboard(), IOhub.send_usbhid(), IOhub.send_gpio())
    except Exception as e:
        raise e
```

---
<a name="setup-and-run"></a>
## Setup and Run 🛠️ 🏃🏼‍♂️

Before running the script using `make`, ensure your system is properly configured with the necessary dependencies and permissions. Follow the steps below:

### 1. System Update and Prerequisites

Update your package lists and upgrade any outdated packages:

```bash
sudo apt-get update && sudo apt-get upgrade
```

Install required development tools and audio libraries:

```bash
sudo apt-get install llvm-dev clang
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install ****python3.11-venv
```

Update and upgrade again just to ensure everything is fresh:

```bash
sudo apt update && sudo apt upgrade
```

### 2. Install Python Environment Dependencies

Install the Python package used for managing environment variables:

```bash
sudo pip3 install python-dotenv
```

### 3. **GPIO Support**

Install the GPIO daemon required for controlling GPIO pins:

```bash
sudo apt install gpiod

```

Reinstall LLVM and Clang just to ensure all required headers and tools are present:

```bash
sudo apt install llvm llvm-dev clang
```

---

### 4. Configure GPIO Pins

Edit your Raspberry Pi’s boot configuration file:

```bash
sudo nano /boot/config.txt

```

Add the following line **at the end of the file**:

```
gpio=17,27=ip,pu
```

🔧 **Explanation:**

This line configures GPIO pins 17 and 27 (change it if you use different pins) as input (`ip`) with pull-down resistors (`pu`). This ensures the pins default to a known highstate (`1`) when you are not sending commands that activate them, which helps avoid unexpected behavior or false triggering of scripts listening to those pins.

This line configures GPIO pins **17 and 27** as **inputs** (`ip`) with **pull-up resistors** (`pu`). That means when nothing is connected to those pins, they will default to a known **high state (1)**.

This is important because your setup uses **relays that are normally open (NO)**, and are **activated by a low signal (0)**. By defaulting the GPIO pins to **high**, we ensure that the relays stay **inactive** when the Raspberry Pi boots or when the pins are left floating — preventing any **unwanted activation**.

🧠 Why this matters:

Each of these relays is wired to control a **"next preset"** command on your **DNAfx** device. So if the GPIO pin were accidentally low (0) at boot, both relays would trigger and unintentionally skip presets/freeze pedal. Setting them high by default avoids this problem.

---

## Environment Configuration (`.env` file) 🧭

Before running the script, make sure to create a `.env` file in the root directory of the project. This file defines key environment variables used by the script.

Here’s the default `.env` file:

```
# Directory where your config JSON file with DNAfx presets is stored
DIR_CONFIG="config/"

# Directory where your recorded looper tracks are stored
DIR_TRACKS="tracks/"

# USB device identifiers for the DNAfx unit
VENDOR_ID="0x0483"
PRODUCT_ID="0x5703"
OUT_ENDPOINT="0x02"

# Enable or disable GPIO relay support
USE_GPIO="ON"

# GPIO pins assigned for 'Next' and 'Back' preset triggers
GPIO_PIN_NEXT="27"
GPIO_PIN_BACK="17"
```

### 🔍 Explanation of Each Variable

- `DIR_CONFIG`
    
    Path to the folder containing your DNAfx **presets config JSON**. This file maps preset names or numbers to their byte values for triggering.
    
- `DIR_TRACKS`
    
    Path to a directory containing **recorded looper tracks** if you're using that functionality.
    
- `VENDOR_ID` and `PRODUCT_ID`
    
    These identify your DNAfx hardware on the USB bus.
    
    If you're unsure of your device's IDs, you can run:
    
    ```bash
    make find_bus
    ```
    
    Which will:
    
    ```
    find_bus:
    	@echo "${GREEN}Finding USB devices${END}"
    	@echo "${YELLOW} You Must create a VENDOR_ID && PRODUCT_ID variable in .env file and assign values:${END}"
    	@echo "${YELLOW}  Example: VENDOR_ID=0483 && PRODUCT_ID=5703${END}"
    	$(SUDO) lsusb
    ```
    
    This command will list all connected USB devices so you can confirm or update the correct vendor/product IDs in your `.env`.
    
- `OUT_ENDPOINT`
    
    The USB output endpoint used for sending messages to the DNAfx. Generally remains `0x02`, but can change it if needed. If unsure use:
    
    ```bash
    make find_bus_verbose
    ```
    
- `USE_GPIO`
    
    Set this to `"ON"` **only if you have the external GPIO relay hardware connected**. Otherwise, set it to `"OFF"`.
    
- `GPIO_PIN_NEXT` and `GPIO_PIN_BACK`
    
    These define which GPIO pins control the **"Next Preset"** and **"Back Preset"** actions. You can remap these if needed based on your circuit.
    

---

## Running ✅

Once everything is installed and configured, you can run the script using:

```bash
make
```

This will build and execute the main script according to the Makefile instructions.

---

## Contributing 🤝

This **is an open source project** — built to be hacked, tweaked, and improved!

If you have ideas, bug fixes, or new features you'd like to add, feel free to jump in. Contributions of any size are welcome and appreciated.

### How to Contribute

1. **Fork** the repository
    
    Click the "Fork" button at the top right of this page to create your own copy.
    
2. **Clone** your fork locally:
    
    ```bash
    bash
    CopyEdit
    git clone git@github.com:your-username/DNAfx_Hack.git
    cd DNAfx_Hack
    ```
    
3. **Create a new branch** for your feature or fix:
    
    ```bash
    bash
    CopyEdit
    git checkout -b my-cool-feature
    ```
    
4. **Make your changes**, commit, and push:
    
    ```bash
    bash
    CopyEdit
    git add .
    git commit -m "Add my cool feature"
    git push origin my-cool-feature
    ```
    
5. **Open a Pull Request**
    
    Go to your fork on GitHub, and click the "Compare & pull request" button.
    

Once your PR is reviewed and approved, it’ll be merged into the main branch. 🎉

---

## Other DNAfx-related project 🧩

## [dnafx-editor](https://github.com/lminiero/dnafx-editor?tab=readme-ov-file) by @lminiero

`dnafx-editor` is an open-source, experimental editor designed for the Harley Benton DNAfx GiT series of guitar pedals, including:

- DNAfx GiT Core
- DNAfx GiT (untested)
- DNAfx GiT Advanced (untested)

---
<a name="disclaimer"></a>
## **Disclaimer**⚠️

This project is neither affiliated with nor endorsed by Harley Benton. It does not intend to replace or compete with the official editor. The tool was developed out of personal necessity and is shared in the hope that others may find it useful and contribute to its development.

**Caution**: As an experimental tool, use `DNAfx_Hack` at your own risk. While it has been regularly tested on the developer's device and appears to function as expected, results may vary in different environments. The developer is not responsible for any potential damage to your device or presets.
