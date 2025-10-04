import { useEffect, useState } from "react";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get-image")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  if (!data) {
    return (
      <div className="flex justify-center items-center h-screen text-white bg-black">
        Loading...
      </div>
    );
  }

  return (
    <div className="w-screen h-screen overflow-hidden bg-black">
      <img
        src={data.hdurl || data.url}
        alt={data.title}
        className="w-full h-full object-cover animate-breathe"
      />
    </div>
  );
};

export default App;
