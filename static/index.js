import React, { useState } from 'react';

const CheckboxForm = () => {
    const optionsList = props.ingredients;

    const list = optionsList.map((label, index) => ({
      id: index + 1,
      label,
      isSelected: false
    }));

    const [options, setOptions] = useState(list);

    const handleChange = (event) => {
      const updatedOptions = options.map(option => {
        if (option.id === parseInt(event.target.value, 10)) {
          return { ...option, isSelected: event.target.checked };
        }
        return option;
      });
      setOptions(updatedOptions);
    };

    const handleSubmit = (event) => {
      event.preventDefault();

      const selectedOptions = options.filter(option => option.isSelected);
      console.log('Selected Options:', selectedOptions);
    };

    const ingredient_form = React.createElement('form', { onSubmit: handleSubmit },
      options.map(option => (
        React.createElement('div', { key: option.id },
          React.createElement('input', {
            type: 'checkbox',
            value: option.id,
            checked: option.isSelected,
            onChange: handleChange
          }),
          React.createElement('label', {}, option.label)
        )
      )),
      React.createElement('button', { type: 'submit' }, 'Submit')
    );
  };

  export default CheckboxForm;