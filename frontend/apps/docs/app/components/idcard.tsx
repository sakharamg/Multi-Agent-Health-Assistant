// Import necessary modules
import React from "react";

const IdCard = ({
  id,
  name,
  age,
  gender,
  icon,
}: {
  id: number;
  name: string;
  age: number;
  gender: string;
  icon: string;
}) => {
  return (
    <div className="bg-blue-100 p-8 rounded-lg shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-blue-800">ID Card</h2>
        <img
          src={icon}
          alt="Profile Picture"
          className="rounded-full h-12 w-12 bg-yellow-200"
        />
      </div>
      <div className="flex justify-between items-center mb-2">
        <span className="font-semibold text-blue-700">ID:</span>
        <span className="text-blue-600">{id}</span>
      </div>
      <div className="flex justify-between items-center mb-2">
        <span className="font-semibold text-blue-700">Name:</span>
        <span className="text-blue-600">{name}</span>
      </div>
      <div className="flex justify-between items-center mb-2">
        <span className="font-semibold text-blue-700">Age:</span>
        <span className="text-blue-600">{age}</span>
      </div>
      <div className="flex justify-between items-center">
        <span className="font-semibold text-blue-700">Gender:</span>
        <span className="text-blue-600">{gender}</span>
      </div>
    </div>
  );
};

export default IdCard;
