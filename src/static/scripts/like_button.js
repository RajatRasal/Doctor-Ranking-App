'use strict';

const domContainer = document.querySelector('#engine');

class DiseaseSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.diseases = props.diseases;
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleOptionSelection = this.handleOptionSelection.bind(this);
  }

  handleOptionSelection(event) {
    console.log(event.target.value);
    this.setState({value: event.target.value});
  }

  handleSubmit() {
    console.log('The selected diseases is: ' + this.state.value);
    if (this.state.value == '') {
      // Update a UI component to say please select an element
      console.log('Nothing is selected');
    } else {
      let disease = this.state.value;
      // disease = disease.replace(/[\W_]+/g, "");
      console.log('HERE ' + disease);
      fetch('/diseases/' + disease, {
        headers: {"Content-Type": "application/json; charset=utf-8"},
        method: 'POST'})
        .then((response) => console.log(response.json()))
	.catch((error) => console.log(error));
    }
  }

  render() {
    const diseaseListItems = this.diseases.map((disease, index) =>
      <option key={index} value={disease}>{disease}</option>
    );
    return (
      <div>
        <h1 className="mt-5">Select Disease</h1>
        <p className="lead">These are all the diseases present in the database. To add more, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p>
	  <div className="input-group">
            <select className="custom-select" onChange={this.handleOptionSelection}>
              <option value="">Choose...</option>
              {diseaseListItems}
            </select>
            <div className="input-group-append">
              <button className="btn btn-outline-secondary" onClick={this.handleSubmit}>Next</button>
            </div>
	  </div>
      </div>
    );
  }
}

function Loader(props) {
  return (
    <div className="d-flex justify-content-center mt-5">
      <div className="spinner-border spinner-border-lg" style={{width: '5rem', height: '5rem'}} role="status">
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  );
}

function fetchDiseases() {
  fetch('/diseases')
    .then(response => {
      if (response.status != 200) {
        console.log("Server Error: " + response.text());
        alert("Server Error: " + response.status);
        return;
      }
      response.json()
        .then(data => {
          console.log(data['diseases']);
          ReactDOM.render(
            <DiseaseSelectionForm diseases={data['diseases']}/>,
            domContainer
           );
        });
    })
    .catch(error => console.log('Fetch error: ' + error)
    );
}

$(document).ready(function() {
  console.log('Loaded page');
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetchDiseases();
});
