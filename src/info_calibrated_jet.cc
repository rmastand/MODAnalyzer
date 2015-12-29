#include "info_calibrated_jet.h"

using namespace std;
using namespace fastjet;


MOD::InfoCalibratedJet::InfoCalibratedJet(std::string tag, double JEC, double area, int number_of_constituents, int charged_multiplicity, double neutral_hadron_fraction, double neutral_em_fraction, double charged_hadron_fraction, double charged_em_fraction) : 
	_tag(tag), 
	_JEC(JEC),
	_area(area),
	_number_of_constituents(number_of_constituents),
	_charged_multiplicity(charged_multiplicity),
	_neutral_hadron_fraction(neutral_hadron_fraction),
	_neutral_em_fraction(neutral_em_fraction),
	_charged_hadron_fraction(charged_hadron_fraction),
	_charged_em_fraction(charged_em_fraction) 
{}


const string MOD::InfoCalibratedJet::tag() const {
  return _tag;
}

const double MOD::InfoCalibratedJet::JEC() const {
	if (_tag == "CMSAK5")
		return _JEC;
	else
		throw runtime_error("Only CMS jets have JEC factors!");
}

const int MOD::InfoCalibratedJet::number_of_constituents() {
	return _number_of_constituents;
}

const int MOD::InfoCalibratedJet::jet_quality() {

	if (_tag != "CMSAK5")
		throw runtime_error("Only CMS jets have jet quality factors!");
	
  // First, check if jet_quality has already been calculated or not. 

  if ((int) _jet_quality == -1) {
    
    // This is the first time we're determining jet quality. Calculate it.

    double cut_offs [3] = { 0.90, 0.95, 0.99 }; // Tight, Medium and Loose.
    
    bool pass = false;

    for (unsigned i = 0; i < 3; i++) {
      
      pass = ( number_of_constituents() > 1 )     &&
             ( neutral_hadron_fraction() < cut_offs[i] ) && 
             ( neutral_em_fraction() < cut_offs[i] )     &&
             ( 
                ( abs(uncorrected_pseudojet().eta()) >= 2.4 ) || 
                ( charged_em_fraction() < 0.99 && charged_hadron_fraction() > 0.00 && charged_multiplicity() > 0) ); 
      
      // UNDETERMINED = -1, FAILED = 0, LOOSE = 1, MEDIUM = 2, TIGHT = 3

      if (pass) {
        _jet_quality =  static_cast<JetQualityLevels_t>(3 - i);
        return _jet_quality;
      }
    } 

    // If the code reached here, this means it didn't pass any quality cut. 
    _jet_quality = static_cast<JetQualityLevels_t>(0);
    
    return _jet_quality;
  }

  return _jet_quality;

}

