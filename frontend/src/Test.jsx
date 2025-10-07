import { useState } from "react";

const Test = () => {
	const [searchValue, setSearchValue] = useState("");
	const [images, setImages] = useState([]);

	function submitFetch() {
		fetchData();
	}

	async function fetchData() {
		const url = `http://127.0.0.1:5000/get-images/${searchValue}`;
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			setImages(data);
		} catch (error) {
			console.error("Error fetching data:", error);
		}
	}

	return (
		<>
			<h1 className="text-3xl font-bold text-center mt-5">NASA API Viewer</h1>
			<hr className="border-t-1 border-white my-4" />
			<div className="flex w-128 gap-6 justify-center mx-auto">
				<input
					type="text"
					placeholder="Search Parameter..."
					className="border border-gray-300 rounded-md p-2 mt-4 w-full hover:border-white transition duration-200"
					value={searchValue}
					onChange={(e) => setSearchValue(e.target.value)}
				/>
				<button
					className="bg-blue-800 hover:bg-blue-600 hover:scale-105 transition duration-200 rounded-md p-2 mt-4 w-36 text-lg"
					onClick={submitFetch}
				>
					Fetch
				</button>
			</div>
			<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-4">
				{images.length > 0 ? (
					images.map((image, index) => (
						<div
							key={index}
							className="border border-gray-300 rounded-md overflow-hidden"
						>
							<img
								src={image}
								alt={`NASA Image ${index + 1}`}
								className="w-full h-auto"
							/>
						</div>
					))
				) : (
					<p className="text-gray-500">No images found.</p>
				)}
			</div>
		</>
	);
};

export default Test;
