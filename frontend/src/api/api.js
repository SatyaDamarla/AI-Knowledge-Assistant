const BASE_URL = "http://127.0.0.1:8000/api";

export const getUserId = () => {
  let userId = localStorage.getItem("user_id");

  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem("user_id", userId);
  }

  return userId;
};

const getHeaders = () => {
  return {
    "X-User-Id": getUserId(),
  };
};

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/sources/upload`, {
    method: "POST",
    headers: getHeaders(),
    body: formData,
  });

  if (!res.ok) {
    throw new Error("PDF upload failed");
  }

  return res.json();
};

export const addText = async (title, text) => {
  const res = await fetch(`${BASE_URL}/sources/text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(),
    },
    body: JSON.stringify({ title, text }),
  });

  if (!res.ok) {
    throw new Error("Text source upload failed");
  }

  return res.json();
};

export const addYouTube = async (title, url) => {
  const res = await fetch(`${BASE_URL}/sources/youtube`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(),
    },
    body: JSON.stringify({ title, url }),
  });

  if (!res.ok) {
    throw new Error("YouTube source upload failed");
  }

  return res.json();
};

export const getSources = async () => {
  const res = await fetch(`${BASE_URL}/sources`, {
    method: "GET",
    headers: getHeaders(),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch sources");
  }

  return res.json();
};

export const queryAPI = async (question, source_ids = []) => {
  const res = await fetch(`${BASE_URL}/chat/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getHeaders(),
    },
    body: JSON.stringify({
      question,
      source_ids,
      top_k: 5,
    }),
  });

  if (!res.ok) {
    throw new Error("Query failed");
  }

  return res.json();
};