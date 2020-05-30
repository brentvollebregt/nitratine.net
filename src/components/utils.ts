export const formatDate = (date: Date) =>
  `${date.getDay()} ${date.toLocaleString("default", { month: "short" })} ${date.getFullYear()}`;
