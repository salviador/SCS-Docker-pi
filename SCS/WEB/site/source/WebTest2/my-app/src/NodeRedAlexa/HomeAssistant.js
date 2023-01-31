import { useState, useRef } from 'react';
import { Container, Navbar, Form, Button, Control, Row, Col, Modal } from 'react-bootstrap';

import "./../App.css";


//const ADDRESS_SERVER = "http://192.168.1.118/";
const ADDRESS_SERVER = "/";


function HomeAssistant() {
    const [flow_anuale, setflow_anuale] = useState("");
    const textAreaRef = useRef(null);




    
    const handle_GeneraManuale = () => {
        const fetchData = async () => {
            await fetch(ADDRESS_SERVER + 'Get_Home_Assistant_Configuration.json')
                .then(res => res.text())
                .then((data) => {
                    console.log(data);
                    setflow_anuale(data);
                });
        };
        fetchData();
    };

    const handle_CopyClipboard = (e) => {
        textAreaRef.current.select();
        document.execCommand('copy');
        // This is just personal preference.
        // I prefer to not show the whole text area selected.
        e.target.focus();
    }

    const handle_codeflow_manuale = () => {
        if (flow_anuale === '') {
            return (
                <>


                </>
            );
        }

        return (
            <>
                <Form.Control as="textarea" rows={10} value={flow_anuale} readonly ref={textAreaRef} />
                <Button variant="outline-primary" onClick={handle_CopyClipboard}>Copy</Button>
            </>
        );
    };





    return (
        <>
            <Container className="justify-content-md-center" style={{}}>
                <div className="pricing-header px-3 py-3 pt-md-5 pb-md-4 mx-auto text-center">
                    <h1 className="display-4">Home Assistant</h1>
                </div>


                <div className="card-deck text-center" >
                    <div className="card mb-4 shadow-sm" style={{ border: "1px solid black" }}>
                        <div className="card-header">
                            <h4 className="my-0 font-weight-normal">Configuration.yaml</h4>
                        </div>
                        <div className="card-body">

                            <ul className="list-unstyled mt-3 mb-4">
                                <li>
                                    <Button variant="outline-primary" onClick={handle_GeneraManuale} >Genera</Button>
                                </li>

                                <li style={{ marginTop: "20px" }}>
                                    {handle_codeflow_manuale()}
                                </li>
                            </ul>




                        </div>
                    </div>
                </div>







            </Container>

        </>
    );
}



export default HomeAssistant;