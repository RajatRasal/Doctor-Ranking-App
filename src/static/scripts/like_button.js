'use strict';

const domContainer = document.querySelector('#disease_selection_form');

function DiseasesList(props) {
  const diseases = props.diseases;
  const listItems = diseases.map((disease, index) =>
    <option key={index} value={disease}>{disease}</option>
  );
  console.log('Diseases List');
  return (
    <select>
      {listItems}
    </select>
  );
}

fetch('/diseases')
  .then(response => {
    if (response.status != 200) {
      console.log("Server Error: " + response.text());
      return;
    }
    response.json()
      .then(data => {
        console.log('THERE');
        console.log(data['diseases']);
        ReactDOM.render(
          <DiseasesList diseases={data['diseases']}/>,
          domContainer
        );
      });
  })
  .catch(error => console.log('Fetch error: ' + error)
  );
