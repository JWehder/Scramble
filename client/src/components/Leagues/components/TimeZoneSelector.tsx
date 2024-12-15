import React, { useState } from "react";
import moment from "moment-timezone";

interface TimeZoneSelectorProps {
  value: string;
  onChange: (zone: string) => void;
  disabled?: boolean;
}

const TimeZoneSelector: React.FC<TimeZoneSelectorProps> = ({
  value,
  onChange,
  disabled = false,
}) => {
  const timeZones = moment.tz.names();
  const [search, setSearch] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setShowDropdown(true); // Ensure dropdown shows when typing
  };

  const handleSelect = (zone: string) => {
    onChange(zone);
    setSearch(""); // Clear search input
    setShowDropdown(false); // Hide dropdown
  };

  const filteredZones = timeZones.filter((tz) =>
    tz.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-2 max-w-48">
      <label className="text-sm font-semibold">Select Time Zone</label>

      {/* Searchable Input */}
      <div className="relative">
        <input
          type="text"
          placeholder="Search for a time zone"
          className="w-full p-2 border rounded focus:ring focus:ring-highlightBlue bg-light text-dark"
          value={search}
          onChange={handleSearch}
          onFocus={() => setShowDropdown(true)} // Show dropdown on focus
          disabled={disabled}
        />

        {/* Dropdown */}
        {showDropdown && filteredZones.length > 0 && (
          <div className="absolute z-10 max-h-64 w-full overflow-y-auto border rounded bg-light shadow-lg">
            {filteredZones.map((zone) => (
              <button
                key={zone}
                onClick={() => handleSelect(zone)}
                className={`block w-full px-4 py-2 text-left hover:bg-highlightBlue hover:text-light ${
                  value === zone ? "bg-highlightBlue text-light" : "text-dark"
                }`}
                disabled={disabled}
              >
                {zone}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Selected Time Zone */}
      {value && (
        <p className="text-sm text-light">
          Selected Time Zone: <span className="font-semibold">{value}</span>
        </p>
      )}
    </div>
  );
};

export default TimeZoneSelector;
