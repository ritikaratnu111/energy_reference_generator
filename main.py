from energy_reference_generator import EnergyReferenceGenerator

def main():
    energy_reference_generator = EnergyReferenceGenerator()
    energy_reference_generator.get_fabric()
    energy_reference_generator.get_testbenches()
    energy_reference_generator.generate_energy()
    return

if __name__ == "__main__":
    main()
