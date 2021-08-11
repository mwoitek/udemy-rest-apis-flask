const getStores = async () => {
  try {
    const response = await fetch('/store');
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
};

getStores();
