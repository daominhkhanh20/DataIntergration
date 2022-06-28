import { useNavigate, useParams } from 'react-router-dom';

export const withRouter = (Component) => {
    const Wrapper = (props) => {
        const params = useParams();
        const navigate = useNavigate();

        return (
            <Component
                navigate={navigate}
                params={params}
                {...props}
            />
        );
    };

    return Wrapper;
};