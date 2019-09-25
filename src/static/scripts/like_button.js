'use strict';

const domContainer = document.querySelector('#engine');

class ParameterSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.params = props.params;
  }

  back(event) {
    fetchDiseases();
  }

  render() {
    const diseaseListItems = this.params.map((pair, index) =>
      <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
        {pair.parameter}
        <span className="badge badge-primary badge-pill">
          {pair.importance}
        </span>
      </li>
    );
    return (
      <div className="container">
        <h1 className="mt-5">Select Parameters</h1>
        <p className="lead">These are all the parameters present in our database. Parameters which have already been selected for a disease have already been ticked and assigned an importance value when they were input. You can remove parameters by setting their importances to 0. All pre-selected or newly selected items are those with values. Any changes to the default will be updated in the database when you click <span className="bold font-italic">Next</span>. To add more parameters for a disease, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p>
	<ul className="list-group list-group-flush m-3">
          {diseaseListItems}
	</ul>
        <div className="row m-2 mt-4">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={this.back}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-secondary">Next</button>
            </span>
          </div>
        </div>
	<ErrorBar error={""} error_message={""}/>
      </div>
    );
  }
}

class DiseaseSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: '',
	          error: props.error,
	          error_message: props.error_message};
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
      console.log('Nothing is selected');
      this.setState({error: 'Input Error',
	             error_message: 'nothing has been selected'});
      return;
    }
    fetchParameters(this.state.value);
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
	<ErrorBar error={this.state.error} error_message={this.state.error_message}/>
      </div>
    );
  }
}

function ErrorBar(props) {
  console.log('HERE');
  console.log(props);
  if (props.error) {
    return (
      <div className="mt-2 alert alert-danger">
        <strong>{props.error}</strong>: {props.error_message}
      </div>
    );
  }
  return (<div/>);
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

function fetchDiseases(error, error_message) {
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/diseases')
    .then(response => {
      if (response.status != 200) {
        console.log("Server Error: " + response.text());
        ReactDOM.render(
          <DiseaseSelectionForm error={response.status}
            error_message={response.text()}/>,
          domContainer
        );
        return;
      }
      response.json()
        .then(data => {
          console.log(data['diseases']);
          ReactDOM.render(
            <DiseaseSelectionForm diseases={data['diseases']} error={error}
              error_message={error_message}/>,
            domContainer
          );
        });
    })
    .catch(error => {
      const error_message = 'could not get diseases';
      console.log('Fetch error: ' + error + ', could not get diseases')
      ReactDOM.render(
        <DiseaseSelectionForm error={error} error_message={error_message}/>,
        domContainer
      );
    });
}

function fetchParameters(disease) {
  console.log('fetching parameters for disease...');
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/diseases/' + disease, {
    headers: {"Content-Type": "application/json; charset=utf-8"},
    method: 'POST'})
    .then(response => {
      if (response.status != 200) {
        const error_message = response.statusText;
        const error_code = response.status;
        console.log('Server Error ' + error_code + ': ' + error_message);
        fetchDiseases('Server error ' + error_code, error_message);
        return;
      }
      response.json()
        .then(data => {
          console.log(data);
          let sortedData = data.sort((a, b) => parseInt(b.importance) - parseInt(a.importance));
          // let x = JSON.parse(data);
          // console.log(typeof x);
          /* console.log(typeof x);
          ReactDOM.render(
            <Parameters params={data[0]}/>,
            domContainer);
          */
          ReactDOM.render(
            <ParameterSelectionForm params={sortedData}/>,
            domContainer
          );
	})
    })
    .catch(error => {
      console.log('Caught error: ' + error)
      fetchDiseases('Fetch error', 'cannot get disease parameters');
    });
}

$(document).ready(function() {
  console.log('Loaded page');
  // fetchDiseases();
  fetchParameters('test disease 1');
});
