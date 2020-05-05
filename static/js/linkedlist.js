alert("zzee");
        region_select = document.getElementById('region');
        municipality_select = document.getElementById('municipality');
        emplacement_select = document.getElementById('emplacement');
         
        region_select.onchange = function(){
         region = region_select.value;
         fetch('municipality/' + region).then(function(response){
          response.json().then(function(data) {
           optionHTML = '';
           for (municipality of data.municipalityregion) {
            optionHTML += '<option value="' + municipality.id +'">' + municipality.name + '</option>'
           }
           municipality_select.innerHTML = optionHTML;
          });
         });
        }
        municipality_select.onchange = function(){
         emplacement = municipality_select.value; 
         fetch('emplacement/' + emplacement).then(function(response){
          response.json().then(function(data) {
           optionHTML = '';
           for (emplacement_rs of data.emplacementlist) {
            optionHTML += '<option value="' + emplacement_rs.id +'">' + emplacement_rs.name + '</option>'
           }
           city_select.innerHTML = optionHTML;
          });
         });
        }