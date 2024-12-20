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
  <div className="rounded-lg overflow-hidden bg-middle shadow-xl w-full">
    <SkeletonTableHeaders columns={columnCount} />
    {Array.from({ length: rowCount }).map((_, idx) => (
      <SkeletonTableRow even={idx % 2 === 0} key={idx} columns={columnCount} />
    ))}
  </div>
);

export default SkeletonTable;
