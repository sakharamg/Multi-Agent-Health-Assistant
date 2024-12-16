import { useEffect, useState } from "react";
import { ENDPOINT } from "../consts/endpoint";

const Reminders = () => {
  const [reminders, setReminders] = useState([]);

  
  // useEffect(()=>fetch(`${ENDPOINT}/eliteapi/send`), [])

  useEffect(() => {
    // const currentTime = Date.now();
    // const intValue = 1733901392462;
    // // Calculate the difference between the current time and the integer value
    // const timeDifference = Math.abs(currentTime - intValue);

    // // Define the desired range in milliseconds (5 minutes)
    // const fiveMinutesRange = 1 * 60 * 1000;

    // // Check if the time difference is within the 5-minute range
    // if (timeDifference <= fiveMinutesRange) {
    //   console.log("The integer value is within the 5-minute range.");
    // } else {
    //   console.log("The integer value is outside the 5-minute range.");
    // }
    fetch(`${ENDPOINT}/eliteapi/getReminders`)
      .then((res) => res.json())
      .then((res) => {
        setReminders(res);
        for(let reminder of res){
          if(reminder.time == "08:00:00"){
            fetch(`${ENDPOINT}/eliteapi/sendReminde/`, {
              method:"POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ reminder: "Hi! It's time for your"+reminder.title }),
            })
          }
        }
      })
      .catch((err) => console.log("Some error occured lol"));
  }, []);
  return (
    <>
      {reminders.length == 0 && (
        <div className="max-w-sm rounded overflow-hidden bg-blue-100 my-2">
          <div className="px-6 py-4">
            <div className="font-bold text-md mb-2">No Reminder to show</div>
          </div>
        </div>
      )}
      {reminders.map((reminder) => (
        <div className="max-w-sm rounded overflow-hidden bg-blue-100 my-2">
          <div className="px-6 py-4">
            <div className="font-bold text-md mb-2">{reminder.title.split("-")[0]}</div>
            <p className="text-gray-700 text-base">{reminder.description}</p>
          </div>
          <div className="px-6 pb-2">
            <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
              Time: {reminder.time}
            </span>
            <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
              Remaining Days: {reminder.remaining_days}
            </span>
          </div>
        </div>
      ))}
    </>
  );
};

export default Reminders;
