export default function CheckList({ element }) {
    return (
        <div>
            <input name="element" type="checkbox" />
            <label htmlFor="element">{element}</label>
        </div>
    )
}