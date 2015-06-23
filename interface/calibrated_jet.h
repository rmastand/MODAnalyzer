#include <iostream>
#include <vector>
#include <string>
#include <iomanip> 
#include <sstream>
#include <ostream>
#include <stdexcept>
#include <cmath>

#include "fastjet/ClusterSequence.hh"


namespace MOD {
   class CalibratedJet {

      public:
         CalibratedJet(double px, double py, double pz, double energy, double mass, std::string algorithm, double JEC);
         CalibratedJet(fastjet::PseudoJet pseudojet, std::string algorithm, double JEC);
         CalibratedJet(std::istringstream & input_stream);
         CalibratedJet();

         fastjet::PseudoJet pseudojet() const;
         
         std::string algorithm() const;
         std::string make_string() const;

         std::string make_header_string() const;

         double mass() const;
         double JEC() const;

         MOD::CalibratedJet corrected_jet();

         friend std::ostream& operator<< (std::ostream&, const CalibratedJet&);

<<<<<<< HEAD
         bool operator<(const CalibratedJet& rhs) const;

=======
>>>>>>> fb4fa903be032715b1351db53399a0357c1f7cf4
      private:
         fastjet::PseudoJet _pseudojet;
         double _mass;
         std::string _algorithm;
         double _JEC;
   };
}