'use client'
import { Dispatch, SetStateAction, useEffect, useState } from "react";
import Loading from "./loadingmodal";

const Summarizer = ({ toggleModal, setToggle }: { toggleModal: boolean, setToggle: Dispatch<SetStateAction<boolean>> }) => {
  const [loading, setLoading] = useState(true)
  
  useEffect(()=>{
    setLoading(true);
    setTimeout(()=>setLoading(false), 3000)
  }, [toggleModal])
  const handleClose = ()=>{
    setToggle(!toggleModal)
  }

  return (
    <div>
      {loading&& toggleModal&&<Loading isLoading={loading} setLoading={setLoading} loaderText="Fetching summary, please wait..." />}
      {!loading && toggleModal && (
        <div className="fixed top-16 z-[100000] flex items-center justify-center">
          <div className="relative max-w-lg w-96 bg-white p-6 rounded-lg shadow-lg">
            <div className="flex justify-between">
              <h3 className="text-lg font-bold">Weekly summary</h3>
              <button onClick={handleClose}>
               <i className="fi fi-sr-x" />
              </button>
            </div>
            <div className="mt-4">
              <table className="w-full border-collapse">
                <thead>
                  <tr>
                    <th className="px-4 py-2 bg-gray-100">Vital</th>
                    <th className="px-4 py-2 bg-gray-100">Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="border px-4 py-2">Avg Oxygen</td>
                    <td className="border px-4 py-2">95</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Steps</td>
                    <td className="border px-4 py-2">27</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Calories</td>
                    <td className="border px-4 py-2">1.02</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Heart Rate</td>
                    <td className="border px-4 py-2">89</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Deep Sleep</td>
                    <td className="border px-4 py-2">54</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Light Sleep</td>
                    <td className="border px-4 py-2">268</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Rem Sleep </td>
                    <td className="border px-4 py-2">118</td>
                  </tr>
                  <tr>
                    <td className="border px-4 py-2">Avg Awake</td>
                    <td className="border px-4 py-2">118</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Summarizer;
