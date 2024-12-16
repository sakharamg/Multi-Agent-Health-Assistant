import { useEffect, useState } from "react";
import { ENDPOINT } from "../consts/endpoint";

const SmartWatch = () => {
  const [date, setDate] = useState(new Date().toLocaleTimeString());
  const [data, setData] = useState({
    oxygen: 100,
    heart_rate: 89,
    steps: 17,
    calories: 0.68,
    sleep: {
      deep: 54,
      light: 268,
      rem: 118,
      awake: 34,
    },
  });
  const setTime = () => {
    setDate(new Date().toLocaleTimeString());
  };
  useEffect(() => {
    const interval = setInterval(() => setTime(), 1000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(
          `${ENDPOINT}/eliteapi/detectAbnormality/`
        );
        const result = await response.json();
        console.log(result)
        setData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const intervalId = setInterval(fetchData, 9000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="h-screen flex items-center justify-center text-white flex-col">
      <div className="w-32 h-48 bg-gray-200 rounded-lg shadow-lg p-4">
        <div className="w-full h-1/3 bg-gray-400 rounded-lg"></div>
        <div className="w-full h-1/3 bg-gray-300 rounded-lg"></div>
        <div className="w-full h-1/3 bg-gray-500 rounded-lg"></div>
      </div>
      <div className="w-full h-72 max-w-xs bg-gray-800 rounded-full shadow-lg p-4 border-8 border-emerald-500">
        <div className="flex items-center justify-center">
          <div className="text-sm font-semibold">{date}</div>
        </div>

        <div className="mt-4 flex items-center justify-center">
          <div className="w-1/2 border-t-2 border-gray-700"></div>
        </div>

        <div className="mt-4 flex items-center justify-center">
          <div className="text-lg font-bold text-emerald-500">
            Samsung Health
          </div>
        </div>

        {/* <div className="mt-4 flex items-center justify-center">
                  <div className="text-sm font-semibold">Weather: Sunny</div>
                </div> */}

        <div className="mt-2 flex items-center justify-center">
          <div className="text-sm font-semibold mr-2">oxygen: {data.oxygen}</div>
          <div className="text-sm font-semibold">heart_rate: {data.heart_rate}</div>
        </div>
        <div className="mt-2 flex items-center justify-center">
          <div className="text-sm font-semibold mr-2">steps: {data.steps}</div>
          <div className="text-sm font-semibold">calories: {data.calories}</div>
        </div>
        <div className="mt-2 flex items-center justify-center flex-col">
          <div className="text-lg font-bold text-blue-400">Sleep</div>
          <div className="text-sm font-semibold">deep: {data.sleep.deep}, light: {data.sleep.light}</div>
          <div className="text-sm font-semibold">rem: {data.sleep.rem}, awake: {data.sleep.rem}</div>
        </div>
      </div>
      <div className="w-32 h-48 bg-gray-200 rounded-lg shadow-lg p-4">
        <div className="w-full h-1/3 bg-gray-500 rounded-lg"></div>
        <div className="w-full h-1/3 bg-gray-300 rounded-lg"></div>
        <div className="w-full h-1/3 bg-gray-400 rounded-lg"></div>
      </div>
    </div>
  );
};

export default SmartWatch;
