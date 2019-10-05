'use strict';

const domContainer = document.querySelector('#engine');

class DisplayDoctorRankings extends React.Component {
  constructor(props) {
    super(props);
    this.state = {downloadLink: "", url: "", download: ""};
    this.doctors = props.doctors;
    this.back = this.back.bind(this);
    this.downloadCsv = this.downloadCsv.bind(this);
  }

  back(event) {
    fetchDoctorLimitCriteria(200, '');
  }

  downloadCsv(event) {
    const downloadLinkElem = document.getElementById('download-link');

    console.log('Generating Top Doctors CSV');
    let topDoctorsCsv = 'Rank,HCP Name,Score\r\n';
    this.doctors['top'].forEach((dict, index) => {
      const row = (index + 1) + ',' + dict['hcp_name'] + ',' + dict['score'] + '\r\n';
      topDoctorsCsv += row;
    });

    console.log('Downloading Top Doctors CSV');
    let blob = new Blob([topDoctorsCsv]);
    let url = window.URL.createObjectURL(blob);
    downloadLinkElem.href = url;
    downloadLinkElem.download = 'top_doctors.csv';
    downloadLinkElem.click();

    console.log('Generating Bottom Doctors CSV');
    let bottomDoctorsCsv = 'Rank,HCP Name,Score\r\n';
    const indexOffset = sessionStorage.getItem('count') - this.doctors['bottom'].length + 1;
    this.doctors['bottom'].forEach((dict, index) => {
      const rowIndex = indexOffset + index;
      const row = rowIndex + ',' + dict['hcp_name'] + ',' + dict['score'] + '\r\n';
      bottomDoctorsCsv += row;
    });

    console.log('Downloading Bottom Doctors CSV');
    blob = new Blob([bottomDoctorsCsv]);
    url = window.URL.createObjectURL(blob);
    downloadLinkElem.href = url;
    downloadLinkElem.download = 'bottom_doctors.csv';
    downloadLinkElem.click();
  }

  render() {
    const topDoctorsTableRows = this.doctors['top'].map((dict, index) =>
      <tr key={index}>
        <th scope="col">{index + 1}</th>
        <td scope="col">{dict['hcp_name']}</td>
        <td scope="col">{dict['score']}</td>
      </tr>
    );
    const indexOffset = sessionStorage.getItem('count') - this.doctors['bottom'].length + 1;
    const bottomDoctorsTableRows = this.doctors['bottom'].map((dict, index) =>
      <tr key={indexOffset + index}>
        <th scope="col">{indexOffset + index}</th>
        <td scope="col">{dict['hcp_name']}</td>
        <td scope="col">{dict['score']}</td>
      </tr>
    );
    return (
      <div className="container">
        <h2 className="mt-5">Doctor Ranking</h2>
        <p className="lead">List of doctors from the top and bottom of the rankings based on the limits you selected on the previous page</p>
        <h4 className="mt-3">Top Doctors</h4>
        <table className="table">
          <thead className="thead-light">
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">HCP Name</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>
            {topDoctorsTableRows}
          </tbody>
        </table>
        <hr className="divider"/>
        <h4 className="mt-3">Bottom Doctors</h4>
        <table className="table">
          <thead className="thead-light">
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">HCP Name</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>
            {bottomDoctorsTableRows}
          </tbody>
        </table>
        <hr className="divider"/>
        <div className="row mt-4">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={this.back}>Back</button>
	        </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-success" onClick={this.downloadCsv}>Download CSV</button>
            </span>
          </div>
        </div>
        <a style={{display: "none"}} target="_blank" href={this.state.url} download={this.state.download} id="download-link">Download Doctor Rankings</a>
      </div>
    );
  }
}

class DoctorLimitSelection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {top: 1, bottom: 0, error: 200, error_message: ''}
    this.maxDoctors = props.doctors;
    this.setTopLimit = this.setTopLimit.bind(this)
    this.setLowerLimit = this.setLowerLimit.bind(this)
    this.next = this.next.bind(this)
    this.back = this.back.bind(this)
  }

  back(event) {
    let disease = sessionStorage.getItem('disease');
    fetchParameters(disease);
  }

  next(event) {
    console.log('Top: ' + this.state.top + ' Bottom: ' + this.state.bottom);
    let error_message = ''
    try {
      if (this.state.top > this.maxDoctors || this.state.top < 1) {
        error_message = 'Top must be between 1 and ' + this.maxDoctors;
        if (this.state.bottom < 0 || this.state.bottom > this.maxDoctors) {
          error_message += ', and bottom must be between 0 and ' + this.maxDoctors;
        }
      } else if (this.state.bottom < 0 || this.state.bottom > this.maxDoctors) {
        error_message = 'Bottom must be between 0 and ' + this.maxDoctors;
      }
    } catch {
      error_message += 'Both limits must be numbers'
    }

    if (error_message != '') {
      console.log(error_message);
      this.setState({error: 200, error_message: error_message});
      return;
    }

    let disease = sessionStorage.getItem('disease');

    console.log('Bottom: ' + this.state.bottom);
    console.log('Top: ' + this.state.top);
    fetchRanking(disease, this.state.top, this.state.bottom);
    console.log('Submit');
  }

  setTopLimit(event) {
    this.setState({top: event.target.value});
  }

  setLowerLimit(event) {
    this.setState({bottom: event.target.value});
  }

  render() {
    return (
      <div className="container">
        <h2 className="mt-5">Select Doctors</h2>
        <p className="lead">Select which doctors to target for your marketing scheme. You can pick from the top ranked doctors or bottom ranked for the specified disease, i.e. Top 5 and Bottom 3, means you will be able to see the top 5 ranked and bottom 3 ranked doctors. <b>The limit is {this.maxDoctors}</b>.</p>
        <div className="row m-3">
	  <div className="col-sm-6 mt-2 mb-3">
            <div className="form-group row">
	      <label htmlFor="top_limit" className="col-sm-4 col-form-label">From top:</label>
	      <div className="col-sm-8">
	        <input onChange={this.setTopLimit} id="top_limit" className="form-control" type="number" defaultValue="1" min="1" max="{this.maxDoctors}"/>
              </div>
            </div>
          </div>
	  <div className="col-sm-6 mt-2 mb-3">
	    <div className="row form-group">
	      <label htmlFor="bottom_limit" className="col-sm-4 col-form-label">From bottom:</label>
	      <div className="col-sm-8">
	        <input onChange={this.setLowerLimit} type="number" className="form-control" id="bottom_limit" defaultValue="0" min="1" max="{this.maxDoctors}"/>
              </div>
            </div>
          </div>
        </div>
        <div className="row m-2">
	    <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={this.back}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-secondary" onClick={this.next}>Next</button>
            </span>
          </div>
        </div>
        <ErrorBar error={this.state.error} error_message={this.state.error_message}/>
      </div>
    );
  }
}

class ParameterSelectionForm extends React.Component {
  constructor(props) {
    super(props);
    this.params = props.params;
    this.back = this.back.bind(this);
    this.next = this.next.bind(this);
  }

  back(event) {
    fetchDiseases(200, '');
  }

  next(event) {
    fetchDoctorLimitCriteria(200, '');
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
        <h2 className="mt-5">Select Parameters</h2>
        <p className="lead">These are all the parameters present in our database. Parameters which have already been selected for a disease have already been ticked and assigned an importance value when they were input. You can remove parameters by setting their importances to 0. All selected parameters are indicated by them having a value. Any change made below, will be updated in the database and set as the default parameter-importance values for this disease when you click <span className="bold font-italic">Next</span>. To add more parameters for a disease, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p>
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
              <button className="btn btn-outline-secondary" onClick={this.next}>Next</button>
            </span>
          </div>
        </div>
	<ErrorBar error={200} error_message={""}/>
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
    this.backToHomepage = this.backToHomepage.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleOptionSelection = this.handleOptionSelection.bind(this);
  }

  handleOptionSelection(event) {
    console.log(event.target.value);
    this.setState({value: event.target.value});
  }

  backToHomepage() {
    displayHomepage();
  }

  handleSubmit() {
    if (this.state.value == '' && this.state.error != 200) {
      this.setState({error_message: 'Error, contact admin to check the server'});
      return;
    }
    if (this.state.value == '' && this.state.error == 200) {
      console.log('Nothing is selected');
      this.setState({error: 200,
                     error_message: 'Input Error, nothing has been selected'});
      return;
    }
    console.log('The selected diseases is: ' + this.state.value);
    fetchParameters(this.state.value);
  }

  render() {
    let diseaseListItems;
    try {
      if (this.diseases) {
        console.log('NOT NULL');
        diseaseListItems = this.diseases.map((disease, index) =>
          <option key={index} value={disease}>{disease}</option>
        );
      } else {
        console.log('NULL');
        diseaseListItems = null;  //(<div></div>);
        console.log('HERE 2');
      }
    }
    catch {
      console.log('UNDEFINED');
      diseaseListItems = null;  // (<div></div>);
    }
    console.log(diseaseListItems);
    return (
      <div>
        <h2 className="mt-5">Select Disease</h2> 
        <p className="lead">These are all the diseases present in the database. To add more, click on the <span className="font-italic">Add/Update Diseases Info</span> tab.</p>
	<div className="row m-1">
          <select className="custom-select" onChange={this.handleOptionSelection}>
            <option value="">Choose...</option>
            {diseaseListItems}
          </select>
	</div>
        <div className="row mt-4">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={this.backToHomepage}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-secondary" onClick={this.handleSubmit}>Next</button>
            </span>
          </div>
        </div>
	<ErrorBar error={this.state.error} error_message={this.state.error_message}/>
      </div>
    );
  }
}

class UploadDiseaseCsv extends React.Component {
  constructor(props) {
    super(props);
    this.state = {error: props.error, error_message: props.error_message};
    this.upload = this.upload.bind(this);
  }

  upload() {
    const files = document.getElementById("uploadDiseasesFile");
    if (files.files && files.files.length == 1) {
      const file = files.files[0]
      uploadDiseaseFile(file);
    } else {
      console.log('Update Error message');
      this.setState({error: 200, error_message: "No file choosen"}); 
    }
    return; 
  }

  render() {
  return (
    <div>
      <h2 className="mt-5">Upload Disease Data file</h2>
      <p className="lead">Select a file containing info about a type of disease and the key parameters which a doctor should be ranked by when consider this disease. The file should be in <code>csv</code> format and be structured as follows:</p>
      <div className="row m-2">
	  <table className="table table-bordered">
	    <thead>
	      <tr>
	        <th scope="col">Disease Name</th>
	        <th scope="col">P1</th>
	        <th scope="col">P1 Weight</th>
	        <th scope="col">...</th>
	        <th scope="col">P4</th>
	        <th scope="col">P4 Weight</th>
	        <th scope="col">...</th>
	        <th scope="col">PN</th>
	        <th scope="col">PN Weight</th>
	      </tr>
	    </thead>
	    <tbody>
	      <tr>
	        <th scope="row">Disease 1</th>
	        <td>Specialization</td>
	        <td>1</td>
	        <td>...</td>
	        <td>Distance</td>
	        <td>5</td>
	        <td>...</td>
	        <td>Hospital</td>
	        <td>4</td>
	      </tr>
	      <tr>
	        <th scope="row">Disease 2</th>
	        <td>Distance</td>
	        <td>5</td>
	        <td>...</td>
	        <td><i>Empty</i></td>
	        <td><i>Empty</i></td>
	        <td>...</td>
	        <td><i>Empty</i></td>
	        <td><i>Empty</i></td>
	      </tr>
	      <tr>
	        <th scope="row">Disease 3</th>
	        <td>Volume of Patients</td>
	        <td>3</td>
	        <td>...</td>
	        <td>Publication</td>
	        <td>2</td>
	        <td>...</td>
	        <td><i>Empty</i></td>
	        <td><i>Empty</i></td>
	      </tr>
	    </tbody>
	  </table>
      </div>
	  <div className="row m-3">
            <input type="file" className="form-control-file" id="uploadDiseasesFile"/>
          </div>
        <div className="row m-2">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={() => displayHomepage()}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-success" onClick={this.upload}>Upload CSV</button>
            </span>
          </div>
        </div>
	<ErrorBar error={this.state.error} error_message={this.state.error_message}/>
    </div>
  );
  }
}

class UploadDoctorsCsv extends React.Component {
  constructor(props) {
    super(props);
    this.state = {error: props.error, error_message: props.error_message};
    this.upload = this.upload.bind(this);
  }

  upload() {
    const files = document.getElementById("uploadDoctorFile");
    if (files.files && files.files.length == 1) {
      const file = files.files[0]
      uploadDiseaseFile(file);
    } else {
      console.log('Update Error message');
      this.setState({error: 200, error_message: "No file choosen"}); 
    }
    return; 
  }

  render() {
  return (
    <div>
      <h2 className="mt-5">Upload Doctors Data file</h2>
      <p className="lead">Select a file containing info about doctors and their weightage factors, which will be factored into out algorithm when ranking doctors for a particular disease. The file should be in <code>csv</code> format and be structured as follows:</p>
      <div className="row m-2">
	  <table className="table table-bordered">
	    <thead>
	      <tr>
	        <th scope="col">Doctor Name</th>
	        <th scope="col">Wt.1</th>
	        <th scope="col">Wt.2</th>
	        <th scope="col">Wt.3</th>
	        <th scope="col">Wt.4</th>
	        <th scope="col">Wt.5</th>
	      </tr>
	    </thead>
	    <tbody>
	      <tr>
	        <th scope="row">Disease 1</th>
	        <td>1</td>
	        <td>2</td>
	        <td>4</td>
	        <td>5</td>
	        <td>3</td>
	      </tr>
	      <tr>
	        <th scope="row">Disease 1</th>
	        <td>5</td>
	        <td>3</td>
	        <td>1</td>
	        <td>2</td>
	        <td>2</td>
	      </tr>
	    </tbody>
	  </table>
      </div>
	  <div className="row m-3">
            <input type="file" className="form-control-file" id="uploadDoctorFile"/>
          </div>
        <div className="row m-2">
          <div className="col-2">
            <span className="float-left">
              <button className="btn btn-outline-secondary" onClick={() => displayHomepage()}>Back</button>
	    </span>
          </div>
          <div className="col-8 text-center">
          </div>
          <div className="col-2">
            <span className="float-right">
              <button className="btn btn-outline-success" onClick={this.upload}>Upload CSV</button>
            </span>
          </div>
        </div>
	<ErrorBar error={this.state.error} error_message={this.state.error_message}/>
    </div>
  );
  }
}

function ErrorBar(props) {
  console.log(props.error + ' ' + props.error_message);
  if (props.error != 200) {
    return (
      <div className="mt-3 alert alert-danger">
        <strong>{props.error}</strong>: {props.error_message}
      </div>
    );
  }
  if (props.error_message != "OK" && props.error_message != "") {
    return (
      <div className="mt-3 alert alert-warning">
        {props.error_message}
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

function Homepage(props) {
  return (
    <div>
      <h1 className="mt-5" align="center">HCP Ranking Engine</h1> 
      <div className="mt-2 mb-2">
      <button type="button" className="btn btn-outline-secondary btn-lg btn-block" onClick={() => fetchDiseases(200, '')}>Rank Doctors</button>
      <button type="button" className="btn btn-outline-secondary btn-lg btn-block" onClick={() => displayUploadDiseaseFile(200, '')}>Add/Update Disease Info</button>
      <button type="button" className="btn btn-outline-secondary btn-lg btn-block" onClick={() => displayUploadDoctorFile(200, '')}>Add/Update Doctors Info</button>
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
      const response_status = response.status;
      const response_statusText = response.statusText;
      if (response_status != 200) {
        const error_message = response_status + ' ' + response_statusText;
        ReactDOM.render(
          <DiseaseSelectionForm error={response_status}
            error_message={response_statusText}/>,
          domContainer
        );
        return;
      }
      if (error != 200) {
        response.json()
          .then(data => {
            console.log(data['diseases']);
            ReactDOM.render(
              <DiseaseSelectionForm diseases={data['diseases']} error={error}
                error_message={error_message}/>,
              domContainer
            );
          });
      } else {
        response.json()
          .then(data => {
            console.log(data['diseases']);
            ReactDOM.render(
              <DiseaseSelectionForm diseases={data['diseases']} error={response_status}
                error_message={response_statusText}/>,
              domContainer
            );
          });
      }
    })
    .catch(error => {
      const error_message = 'user end fetch error, could not get diseases';
      console.log('Fetch error: ' + error + ', could not get diseases')
      ReactDOM.render(
        <DiseaseSelectionForm error={0} error_message={error_message}/>,
        domContainer
      );
    });
}

function fetchParameters(disease) {
  console.log('fetching parameters for disease...');
  sessionStorage.setItem('disease', disease);
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
        console.log('Server Error' + error_code + ': ' + error_message);
        fetchDiseases('Server error', error_code + ' ' + error_message);
        return;
      }
      response.json()
        .then(data => {
          console.log(data);
          let sortedData = data.sort((a, b) => parseInt(b.importance) - parseInt(a.importance));
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

function fetchDoctorLimitCriteria() {
  console.log('fetching max number of doctors to select from...');
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/doctors/count')
    .then(response => {
      if (response.status != 200) {
        const error_message = response.statusText;
        const error_code = response.status;
        console.log('Server Error' + error_code + ': ' + error_message);
        let disease = sessionStorage.getItem('disease');
        fetchParameters(disease);
        return;
      }
      response.json()
        .then(data => {
          sessionStorage.setItem('count', data['count']);
          ReactDOM.render(
            <DoctorLimitSelection doctors={data['count']}/>,
            domContainer
          )
       })
    })
}

function fetchRanking(disease, top_limit, bottom_limit) {
  console.log('fetching max number of doctors to select from...');
  sessionStorage.setItem('upper_limit', top_limit);
  sessionStorage.setItem('lower_limit', bottom_limit);
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/doctors/rank/' + disease + '/' + top_limit + '/' + bottom_limit)
    .then(response => {
      if (response.status != 200) {
        const error_message = response.statusText;
        const error_code = response.status;
        alert('Server Error' + error_code + ': ' + error_message);
        fetchDoctorLimitCriteria();
        return;
      }
      response.json()
        .then(data => {
	  console.log(data);
          ReactDOM.render(
            <DisplayDoctorRankings doctors={data}/>,
            domContainer
          );
	});
      }
    );
}

function uploadDiseaseFile(file) {
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  fetch('/diseases/upload', {
    headers: {"Content-Type": "text/csv; charset=utf-8"},
    method: 'POST',
    body: file})
    .then(response => {
      console.log('HERE');
      if (!response.ok) {
        alert('Disease file upload: ' + response.status);
        ReactDOM.render(<UploadDiseaseCsv/>, domContainer);
        return;
      }
      alert('Changes successful!');
      displayHomepage()
    })
    .catch(error => {
      console.log('Disease file upload error: ' + error);
      // Add error message to upload disease csv form
      ReactDOM.render(<UploadDiseaseCsv/>, domContainer);
    });
}

function displayUploadDiseaseFile(error, error_message) {
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  ReactDOM.render(
    <UploadDiseaseCsv error={error} error_message={error_message}/>,
    domContainer
  );
}

function displayUploadDoctorFile(error, error_message) {
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  console.log('ERRORS:' + error, + ' ' + error_message);
  ReactDOM.render(
    <UploadDoctorsCsv error={error} error_message={error_message}/>,
    domContainer
  );
}

function displayHomepage() {
  console.log('Loading homepage...');
  ReactDOM.render(
    <Loader/>,
    domContainer
  );
  console.log('Displaying homepage...');
  ReactDOM.render(
    <Homepage/>,
    domContainer
  );
}


$(document).ready(function() {
  console.log('Loaded page');
  displayHomepage();
  // displayUploadDiseaseFile();
  // fetchDiseases(200, '');
  // fetchParameters('test disease 1');
  // fetchDoctorLimitCriteria();
  // sessionStorage.setItem('upper_limit', 1);
  // sessionStorage.setItem('lower_limit', 0);
  // sessionStorage.setItem('count', 26);
  // fetchRanking('test disease 1', 2, 3);
});
