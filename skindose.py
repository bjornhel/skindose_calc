from pyskindose import (
    PyskindoseSettings,
    load_settings_example_json,
    print_available_human_phantoms,
    get_path_to_example_rdsr_files,
    print_example_rdsr_files,
)
from pyskindose.main import main


# Parse the settings to a setting class:
settings_json = load_settings_example_json()
settings = PyskindoseSettings(settings=settings_json)

# settings.print_parameters()

# print(settings.__doc__)  # uncomment this line to read about settings.general
# print(settings.phantom.__doc__) # uncomment this line to read about settings.phantom
# print(settings.phantom.patient_offset.__doc__)  # uncomment this line to read about settings.phantom.patient_offset
# print(settings.phantom.dimension.__doc__) # uncomment this line to read about settings.phantom.dimension
# print(settings.plot.__doc__) # uncomment this line to read about settings.plot
# print(settings.normalization_settings.__doc__) # uncomment this line to read about settings.normalisation_settings

# Example 1:
"""
settings = PyskindoseSettings(settings=load_settings_example_json())
settings.mode = "plot_setup"
settings.phantom.model = "cylinder"

# Uncomment any of the following lines to translate the position of the phantom:
# settings.phantom.patient_offset.d_lat = -20
# settings.phantom.patient_offset.d_lon = +10
# settings.phantom.patient_offset.d_ver = -10

main(settings=settings)
"""

# Example 2:
"""
settings = PyskindoseSettings(settings=load_settings_example_json())
settings.mode = "plot_setup"

# Select an elliptical cylinder with length 150 cm and a
# radius of[20, 10] cm
# settings.phantom.model = "cylinder"
# settings.phantom.dimension.cylinder_length = 150
# settings.phantom.dimension.cylinder_radii_a = 20
# settings.phantom.dimension.cylinder_radii_b = 10

# Select a planar phantom with length 120 cm and width 40 cm
# settings.phantom.model = "plane"
# settings.phantom.dimension.plane_length = 120
# settings.phantom.dimension.plane_width = 40

# Select a human phantom
settings.phantom.model = "human"
settings.phantom.human_mesh = "hudfrid"

main(settings=settings)
"""

# print_available_human_phantoms()

# print_example_rdsr_files()

# Example 3:
"""
settings = PyskindoseSettings(settings=load_settings_example_json())
settings.mode = "plot_procedure"
settings.phantom.model = "cylinder"

rdsr_data_dir = get_path_to_example_rdsr_files()

# You can set the maximum number of irradiation events for including the
# phantom in the plot. Here, we set it to 0 to reduce memory use.
settings.plot.max_events_for_patient_inclusion = 0

# Change this path to use your own RDSR file
# N.B: If your are using a windows OS, you need to set the path as r raw string,
# for example:
# selected_rdsr_filepath = Path(r'c:\rdsr_files\file_name.dcm')
selected_rdsr_filepath = rdsr_data_dir / "siemens_axiom_example_procedure.dcm"

main(settings=settings, file_path=selected_rdsr_filepath)
"""
# Example 4:
"""
settings = PyskindoseSettings(settings=load_settings_example_json())
settings.mode = "calculate_dose"
settings.output_format = 'html' # set output format to html
settings.plot.plot_dosemap = True # enable dosemap plot
settings.phantom.model = "human"
settings.phantom.human_mesh = "hudfrid"


settings.phantom.patient_offset.d_lat = -35
rdsr_data_dir = get_path_to_example_rdsr_files()
selected_rdsr_filepath = rdsr_data_dir / "siemens_axiom_example_procedure.dcm"
main(settings=settings, file_path=selected_rdsr_filepath)
"""
# Example 5:
settings = PyskindoseSettings(settings=load_settings_example_json())
settings.mode = "calculate_dose"
settings.output_format = 'dict'

rdsr_data_dir = get_path_to_example_rdsr_files()
output = main(settings=settings, file_path=rdsr_data_dir / "siemens_axiom_example_procedure.dcm")

print(f'estimated psd {output["psd"].round(1)} mGy')