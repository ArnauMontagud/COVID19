#include "./internal-viral-response.h" 

using namespace PhysiCell; 

// inputs: 

// outputs: 

void internal_virus_response_model( Cell* pCell, Phenotype& phenotype, double dt )
{
	// bookkeeping -- find microenvironment variables we need

	static int nE = microenvironment.find_density_index( "virion" ); 
	static int nUV = microenvironment.find_density_index( "uncoated virion" ); 
	static int nR = microenvironment.find_density_index( "viral RNA" ); 
	static int nP = microenvironment.find_density_index( "viral protein" ); 
	static int nA = microenvironment.find_density_index( "assembled virion" ); 

	// bookkeeping -- find custom data we need 
	
	
	// actual model goes here 

	
	

	// now, set apoptosis rate 
	
	static int apoptosis_model_index = cell_defaults.phenotype.death.find_death_model_index( "Apoptosis" );
	phenotype.death.rates[apoptosis_model_index] = pCell->custom_data["max_infected_apoptosis_rate"] ; 
	
	double v = phenotype.molecular.internalized_total_substrates[nA] /
		pCell->custom_data["max_apoptosis_half_max"] ; 
	v = pow( v, pCell->custom_data["apoptosis_hill_power"] ); 
	
	double effect = v / (1.0+v); 
	phenotype.death.rates[apoptosis_model_index] *= effect; 
	
	// record data as needed 
	
	
	return; 
}
