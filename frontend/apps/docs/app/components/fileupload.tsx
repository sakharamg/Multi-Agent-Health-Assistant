import { Button } from "@chatscope/chat-ui-kit-react";
import React from "react";
import { useDropzone } from "react-dropzone";
import styled from "styled-components";
import { ENDPOINT } from "../consts/endpoint";

const getColor = (props) => {
  if (props.isDragAccept) {
    return "#00e676";
  }
  if (props.isDragReject) {
    return "#ff1744";
  }
  if (props.isFocused) {
    return "#2196f3";
  }
  return "#eeeeee";
};

const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 300px;
  align-items: center;
  padding: 10px;
  border-width: 2px;
  border-radius: 2px;
  border-color: ${(props) => getColor(props)};
  border-style: dashed;
  background-color: #fafafa;
  color: #bdbdbd;
  outline: none;
  transition: border 0.24s ease-in-out;
`;

function FileUpload() {
  const {
    getRootProps,
    getInputProps,
    isFocused,
    isDragAccept,
    isDragReject,
    acceptedFiles,
  } = useDropzone({ accept: { "image/*": [] } });
  const files = acceptedFiles.map((file) => (
    <div key={file.path}>
      {file.path} - {file.size} bytes
    </div>
  ));
  const handleUpload = () => {
    for (let file of acceptedFiles) {
      if (file.path == "./cough.jpg") {
        fetch(`${ENDPOINT}/eliteapi/createReminder/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: {
              patientName: "Michael Jackson",
              medications: [
                {
                  medicineName: "tminic cough relief& asthakind",
                  dosage: "2 spoon",
                  frequency: "Before each meal",
                  duration: "7 days",
                },
              ],
            },
          }),
        });
      }
    }
  };

  return (
    <div className="container flex">
      <Container {...getRootProps({ isFocused, isDragAccept, isDragReject })}>
        {files.length == 0 && (
          <>
            {" "}
            <input {...getInputProps()} />
            <p>Drag 'n' drop your prescription here</p>
          </>
        )}
        <aside>{files}</aside>
      </Container>
      <Button onClick={handleUpload}>Upload</Button>
    </div>
  );
}

export default FileUpload;
