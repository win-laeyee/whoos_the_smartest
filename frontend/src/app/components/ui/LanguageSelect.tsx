import { LanguageSelectProps } from "../../interfaces/props";

const LanguageSelect: React.FC<LanguageSelectProps> = ({
  language,
  handleChange,
}) => {
  return (
    <label className="form-control w-full ">
      <div className="label">
        <span className="label-text font-semibold">
          {" "}
          Select preferred language for the notes
        </span>
      </div>
      <select
        name="language"
        value={language}
        onChange={handleChange}
        className="select select-bordered rounded-full border-black border-2 w-full mb-2"
      >
        <option value="" disabled></option>
        <option value="Arabic">Arabic</option>
        <option value="Bengali">Bengali</option>
        <option value="Bulgarian">Bulgarian</option>
        <option value="Chinese simplified and traditional">
          Chinese (Simplified & Traditional)
        </option>
        <option value="Croatian">Croatian</option>
        <option value="Czech">Czech</option>
        <option value="Danish">Danish</option>
        <option value="Dutch">Dutch</option>
        <option value="English">English</option>
        <option value="Estonian">Estonian</option>
        <option value="Finnish">Finnish</option>
        <option value="French">French</option>
        <option value="German">German</option>
        <option value="Greek">Greek</option>
        <option value="Hebrew">Hebrew</option>
        <option value="Hindi">Hindi</option>
        <option value="Hungarian">Hungarian</option>
        <option value="Indonesian">Indonesian</option>
        <option value="Italian">Italian</option>
        <option value="Japanese">Japanese</option>
        <option value="Korean">Korean</option>
        <option value="Latvian">Latvian</option>
        <option value="Lithuanian">Lithuanian</option>
        <option value="Norwegian">Norwegian</option>
        <option value="Polish">Polish</option>
        <option value="Portuguese">Portuguese</option>
        <option value="Romanian">Romanian</option>
        <option value="Russian">Russian</option>
        <option value="Serbian">Serbian</option>
        <option value="Slovak">Slovak</option>
        <option value="Slovenian">Slovenian</option>
        <option value="Spanish">Spanish</option>
        <option value="Swahili">Swahili</option>
        <option value="Swedish">Swedish</option>
        <option value="Thai">Thai</option>
        <option value="Turkish">Turkish</option>
        <option value="Ukrainian">Ukrainian</option>
        <option value="Vietnamese">Vietnamese</option>
      </select>
    </label>
  );
};

export default LanguageSelect;
