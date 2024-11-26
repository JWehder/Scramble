import React from "react";
import SkeletonTableHeaders from "./SkeletonTableHeaders";
import SkeletonTableRow from "./SkeletonTableRow";

interface SkeletonTableProps {
  rowCount?: number;
  columnCount?: number;
}

const SkeletonTable: React.FC<SkeletonTableProps> = ({
  rowCount = 5,
  columnCount = 4,
}) => (
  <div className="rounded-lg overflow-hidden bg-dark">
    <SkeletonTableHeaders columns={columnCount} />
    {Array.from({ length: rowCount }).map((_, idx) => (
      <SkeletonTableRow key={idx} columns={columnCount} />
    ))}
  </div>
);

export default SkeletonTable;
