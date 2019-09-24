'use strict';

const domContainer = document.querySelector('#engine');

function DiseasesList(props) {
  const diseases = props.diseases;
  return (
    <select>{listItems}</select>
  );
}

class DiseaseSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.diseases = props.diseases;
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    const diseaseListItems = this.diseases.map((disease, index) =>
      <option key={index} value={disease}>{disease}</option>
    );
    return (
      <div>
        <h1 className="mt-5">Select Disease</h1>
        <p className="lead">These are all the diseases present in the database. To add more, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p> 
        <form onSubmit={this.handleSubmit}>
	  <div className="input-group">
            <select className="custom-select">
              <option selected>Choose...</option> 
              {diseaseListItems}
            </select>
            <div className="input-group-append">
              <button className="btn btn-outline-secondary" type="submit">Next</button>
            </div>
	  </div>
        </form>
      </div>
    );
  }
}

const diseases = fetch('/diseases')
  .then(response => {
    if (response.status != 200) {
      console.log("Server Error: " + response.text());
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
