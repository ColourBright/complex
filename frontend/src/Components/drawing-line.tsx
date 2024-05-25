type DrawingLineProps = {
    height: number,
    width: number,
    graphHeight: number,
    graphWidth: number,
    line: [number, number][]
}

export const DrawingLine = ({height, width, graphHeight, graphWidth, line}: DrawingLineProps) => {
    const pixelsInCellW = width / graphWidth;
    const pixelsInCellH =  height / graphHeight;
    const pathData = "M " + line.map(p => {
        return `${(p[0] + graphWidth / 2) * pixelsInCellW} ${(-p[1] + graphHeight / 2) * pixelsInCellH}`
    })
        .join(" L ");
    return <path className="path" d={pathData} fill={'transparent'} stroke={'black'} strokeWidth={3}/>;
}