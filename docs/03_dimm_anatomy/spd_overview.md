# SPD Overview: Configuration, Discovery, and Bring-Up

This document explains the role of **SPD (Serial Presence Detect)** on a DDR DIMM, how it is used during system bring-up, and why correct SPD data is essential for memory correctness.

Without SPD, a DIMM cannot be safely or reliably used in a modern system.

---

## What SPD Is

SPD is a small non-volatile memory device (typically an EEPROM) located on the DIMM.

It stores **descriptive and configuration data** about the memory module, including:

- Capacity and organization
- Supported timings
- Voltage requirements
- DRAM device characteristics
- Manufacturer and revision information

SPD allows the system to discover *what the DIMM is* before attempting to use it.

---

## Why SPD Exists

Modern systems must support:

- Multiple DIMM capacities
- Different DRAM organizations
- Varying timing capabilities
- Multiple vendors and revisions

Hard-coding memory parameters is not viable.

SPD enables:

- Automatic configuration
- Safe initialization
- Platform independence

It is the handshake between the DIMM and the memory controller.

---

## Where SPD Lives

SPD is implemented as:

- A dedicated EEPROM on the DIMM
- Connected via a low-speed serial bus (I²C / SMBus)

It is powered whenever standby power is available, allowing:

- Early access during boot
- Configuration before DRAM is enabled

SPD operates independently of the DRAM core.

---

## What Information SPD Provides

While exact contents depend on DDR generation, SPD generally includes:

### Structural Information

- Total memory size
- Number of ranks
- Device width and density
- Bank and row organization

This allows the controller to correctly map addresses.

---

### Electrical and Timing Information

- Supported CAS latencies
- Minimum timing parameters
- Voltage levels
- Refresh requirements

These values define **safe operating points**, not aggressive ones.

---

### Optional Profiles

Some DIMMs include additional profiles:

- Enhanced timing sets
- Performance-oriented configurations

These are optional and not required for correctness.

OMI focuses on **baseline, standards-compliant SPD data**.

---

## SPD and Memory Bring-Up Sequence

A simplified bring-up sequence looks like:

1. System powers on
2. Firmware reads SPD data
3. Memory controller configures:
   - Address mapping
   - Timings
   - Voltages
4. DRAM initialization sequence begins
5. Basic memory tests are run
6. System proceeds to normal operation

If SPD data is incorrect, failure occurs **before software is involved**.

---

## Why Incorrect SPD Is Dangerous

Incorrect or inconsistent SPD data can cause:

- Overly aggressive timings
- Incorrect voltage configuration
- Wrong address decoding
- Incomplete refresh scheduling

These failures often:

- Appear intermittent
- Depend on temperature or load
- Pass basic tests
- Fail later in operation

Because SPD is trusted implicitly, errors propagate silently.

---

## SPD Is a Contract, Not a Suggestion

The memory controller assumes:

- SPD data is correct
- SPD data is conservative
- SPD data reflects worst-case behavior

Controllers do not verify SPD against reality.
They configure memory based on trust.

This makes SPD part of the **correctness boundary**.

---

## SPD and Interoperability

SPD enables:

- Cross-platform compatibility
- Vendor independence
- Safe mixing of DIMMs

Without SPD:

- Manual tuning would be required
- Validation burden would explode
- Reliability would collapse

SPD is essential for scalable systems.

---

## Implications for OMI

OMI treats SPD as:

- A required design artifact
- A documented interface
- A reproducibility requirement

For OMI v1:

- SPD contents must be published
- Assumptions must be explained
- Conservative parameters must be justified

Open memory requires open configuration.

---

## What OMI Does Not Optimize

OMI does not:

- Push aggressive SPD timings
- Optimize for benchmark performance
- Encode vendor-specific tricks

OMI prioritizes:

- Correctness
- Clarity
- Reproducibility

SPD reflects that philosophy.

---

## Takeaway

SPD is how a DIMM introduces itself to the system.

It defines:

- What the memory is
- How it should be used
- What margins are required

Incorrect SPD turns a correct design into a fragile one.

OMI documents SPD to make memory bring-up understandable and trustworthy.
