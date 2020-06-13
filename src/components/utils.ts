export const formatDate = (date: Date) =>
  `${date.getDate()} ${date.toLocaleString("default", { month: "short" })} ${date.getFullYear()}`;

export const truncateString = (string: string, maxLength: number) => {
  if (string.length <= maxLength) {
    return string;
  }
  return `${string.substring(0, maxLength)}...`;
};
