const API_URL = 'http://localhost:5000/api';

export const recognizeSpeech = async (fileUrl) => {
  try {
    const response = await fetch(`${API_URL}/recognize/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ file: fileUrl }),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error recognizing speech:', error);
    throw error;
  }
};