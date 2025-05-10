/**
 * Formats an ISO 8601 timestamp (which might include microseconds)
 * into an absolute long date string using Intl.DateTimeFormat.
 *
 * @param {string} timestamp - The ISO 8601 timestamp string.
 * @param {string} [locale='en-US'] - The locale used for formatting.
 * @param {string} [timeZone='Asia/Manila'] - The time zone used for formatting.
 * @returns {string} The formatted long date string.
 *
 * @example
 * const longDate = formatLongDate("2025-05-06T22:15:54.719804+08:00");
 * console.log(longDate); // "May 6, 2025"
 */
function formatLongDate(timestamp, locale='en-US', timeZone='Asia/Manila') {
    // Truncate microseconds to milliseconds (only the first three digits after the decimal)
    const truncatedTimestamp = timestamp.replace(/(\.\d{3})\d+/, '$1');

    // Create a Date instance from the modified timestamp
    const dateObj = new Date(truncatedTimestamp);

    // Use Intl.DateTimeFormat with the 'long' date style to format the date.
    const formattedDate = new Intl.DateTimeFormat(locale, {
        dateStyle: 'long',
        timeZone
    }).format(dateObj);

    return formattedDate;
}

// Export the utility function for use in other modules.
export { formatLongDate };