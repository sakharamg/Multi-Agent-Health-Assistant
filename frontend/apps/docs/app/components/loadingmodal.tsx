import React, { useState } from 'react';

function Loading({isLoading, setLoading, loaderText}) {

  const toggleLoadingModal = () => {
    console.log("here")
    setLoading(!isLoading);
  };

  return (
    <div className="App">
      {/* <button onClick={toggleLoadingModal} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Toggle Loading Modal
      </button> */}

      {isLoading && (
        <div className="absolute top-0 left-0 z-[200000] flex items-center justify-center bg-black bg-opacity-50 w-[100vw] h-[100vh]">
          <div className="relative max-w-lg w-full bg-white p-6 rounded-lg shadow-lg">
            <div className="flex items-center justify-center h-32">
              <div className="w-10 h-10 border-t-2 border-blue-400 rounded-full animate-spin"></div>
            </div>
            <div className="mt-4 text-center">
              <p className="text-gray-700">{loaderText}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Loading;