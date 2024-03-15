import {Footer, FooterLink, FooterLinks, FooterText} from 'react-weui';

const SuccessFooter = ({links, copyright}) => (
    <Footer className="footer">
        <FooterLinks>
            {links.map((link, index) => (
                <FooterLink key={index} href={link.href}>{link.text}</FooterLink>
            ))}
        </FooterLinks>
        <FooterText>
            {copyright}
        </FooterText>
    </Footer>
);

export default SuccessFooter;
